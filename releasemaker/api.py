# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import requests
from urllib import urlencode

from releasemaker.exceptions import ResourceNotFound
from releasemaker.structures import PullRequest, Issue


class GitHubRepo(object):
    """Handles interaction with a specific repository through the GitHub API."""

    def __init__(self, repo_owner, repo_name, access_token):
        """
        :param repo_owner:
                Slug of the repository owner.
        :param repo_name:
                Slug of the repository.
        :param access_token:
                Access token that we can use to interface with the GitHub API.
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.access_token = access_token

    def get_all(self, endpoint, params=None):
        """Traverses all pages of this API call to return all data."""
        merged_json = []

        # Continue fetching pages until we reach an empty one. GitHub doesn't return a count of the total number of
        # pages, so there's no alternative.
        page = 1
        get_next_page = True
        while get_next_page:
            json = self.get(endpoint, page, params)
            merged_json += json
            if not len(json) > 0:
                get_next_page = False
            page += 1

        return merged_json

    def get(self, endpoint, page=1, params=None):
        """Files a GET request against the GitHub API. Returns a Response objects from the requests library."""
        url = 'https://api.github.com/%(endpoint)s?access_token=%(token)s&page=%(page)d' % {
            'endpoint': endpoint,
            'token': self.access_token,
            'page': page,
        }
        if params is not None:
            url += '&' + urlencode(params)
        response = requests.get(url)

        # Produce specific error on 404. Generic HTTPError otherwise.
        if response.status_code == 404:
            raise ResourceNotFound
        response.raise_for_status()

        return response.json()

    def get_open_pull_requests(self, required_labels=None):
        """
        Returns a list of `PullRequest` objects. Two types of API calls have to be made. The pull request list is
        downloaded in its entirety. The list of labels for each pull request isn't included in this API call, so we
        have to retrieve these using a separate call for each pull request.

        :param required_labels:
                Any pull requests that don't carry all labels in this list will be filtered.
        """
        json = self.get_all('repos/%(owner)s/%(repo)s/pulls' % {
            'owner': self.repo_owner,
            'repo': self.repo_name,
        }, params={
            'direction': 'asc',
        })
        required_labels = required_labels or []

        prs = []
        for pr_data in json:
            # Construct the pull request and issue data structures
            pr_id = pr_data['number']
            issue_obj = self.get_issue(pr_id)
            pr_obj = PullRequest(pr_id, pr_data['title'], pr_data['body'], pr_data['head']['ref'],
                                 pr_data['html_url'], pr_data['created_at'], pr_data['updated_at'], issue_obj)

            # Check if the PR survives the filters
            include_pr = True
            for required_label in required_labels:
                if not pr_obj.has_label(required_label):
                    include_pr = False
                    break
            if include_pr:
                prs.append(pr_obj)

        return prs

    def get_issue(self, issue_id):
        """Fetches an issue and returns an `Issue` object. None if non-existent."""
        try:
            json = self.get('repos/%(owner)s/%(repo)s/issues/%(issue_id)d' % {
                'owner': self.repo_owner,
                'repo': self.repo_name,
                'issue_id': issue_id,
            })

            label_list = [label_dict['name'] for label_dict in json['labels']]

            return Issue(json['number'], label_list)
        except ResourceNotFound:
            return None
