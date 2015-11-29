# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from dateutil import parser


class PullRequest(object):
    """Contains the state of a pull request on GitHub."""
    def __init__(self, pr_id, title, body, branch_name, link, created, updated, issue=None):
        """
        :param pr_id:
                ID of the pull request.
        :param title:
                Title of the pull request.
        :param body:
                Description of the pull request.
        :param branch_name:
                Name of the branch that the pull request would merge, as it is shown on GitHub.
        :param link:
                URI of the pull request. It's GitHub's standard pull request detail page, so it's human-readable.
        :param created:
                Raw string indicating when the pull request was created.
        :param updated:
                Raw string indicating when the pull request was last updated.
        :param issue:
                Link to the associated `Issue` object. Even if you don't use GitHub's issue tracking, pull requests
                can have this.
        :return:
        """
        self.pr_id = pr_id
        self.title = title
        self.body = body
        self.branch_name = branch_name
        self.link = link
        self.created = parser.parse(created)
        self.updated = parser.parse(updated)
        self.issue = issue

    def __str__(self):
        return self.title

    def unicode_multiline(self):
        """A multiline unicode representation of this pull request."""
        multiline = [
            '[#%d] %s' % (self.pr_id, self.title),
            'Branch: %s' % self.branch_name,
            'Link: %s' % self.link,
        ]
        if self.issue:
            multiline.append('Labels: %s' % ', '.join(self.issue.labels))
        if self.body:
            multiline.append('')
            multiline.append(self.body)

        return multiline

    def has_label(self, label_name):
        """Returns boolean indicating whether or not this pull request carries a certain label."""
        if not self.issue:
            return False
        else:
            return label_name in self.issue.labels


class Issue(object):
    """Contains the state of an issue on GitHub."""
    def __init__(self, issue_id, labels):
        self.issue_id = issue_id
        self.labels = labels

    def __str__(self):
        return 'Issue #%d' % self.issue_id
