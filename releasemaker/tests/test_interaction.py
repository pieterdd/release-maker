# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from contextlib import contextmanager
import csv
import os
from unittest import TestCase
from releasemaker.cli_io import prepare_release
from releasemaker.api import GitHubRepo
from releasemaker.factories import PullRequestFactory
from releasemaker.git import GitInterface
from mock import patch, call


class InteractionTest(TestCase):
    """
    Performs an automated runthrough of the release prepping script, while mocking out GitHub API integration and faking
    the git commands that would be executed.
    """
    def setUp(self):
        self.target_branch_name = 'release-1234'

        self.ask_token_patch = patch('releasemaker.cli_io.ask_api_token', return_value='123456')
        self.infer_repo_details_patch = patch.object(GitInterface, 'infer_repo_details',
                                                     return_value=('owner', 'reponame'))
        self.tracked_file_patch = patch.object(GitInterface, 'tracked_files_changed', return_value=False)
        self.call_in_repo_patch = patch.object(GitInterface, 'call_in_repo_dir')
        self.check_output_in_repo_patch = patch.object(GitInterface, 'check_output_in_repo_dir')
        self.ask_target_branch_patch = patch('releasemaker.cli_io.ask_target_branch', return_value=self.target_branch_name)
        self.ask_filter_labels_patch = patch('releasemaker.cli_io.ask_filter_labels', return_value=['Ready'])
        self.get_open_prs_patch = patch.object(GitHubRepo, 'get_open_pull_requests', return_value=[])
        self.ask_include_pr = patch('releasemaker.cli_io.ask_include_pr', return_value=True)
        self.ask_export_csv = patch('releasemaker.cli_io.ask_export_csv', return_value=True)

    @contextmanager
    def activate_mocks(self):
        with self.ask_token_patch, self.infer_repo_details_patch, self.tracked_file_patch,\
              self.call_in_repo_patch as self.call_in_repo_mock,\
              self.check_output_in_repo_patch, self.ask_target_branch_patch, self.ask_filter_labels_patch,\
              self.get_open_prs_patch, self.ask_include_pr, self.ask_export_csv:
            yield

    def inspect_and_delete_csv(self, expected_rows):
        """
        Ensure the contents of a CSV file to see if the contents align with the expected values. Then removes it from
        disk to avoid unit test leftovers.
        """
        csv_file_name = '%s.csv' % self.target_branch_name
        with open(csv_file_name, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            actual_rows = list(csv_reader)
            self.assertListEqual(actual_rows, expected_rows)
        os.remove(csv_file_name)

    def assert_git_commands_ran(self, prs):
        """
        Given a set of pull requests that should have been merged into a release branch, checks if the appropriate Git
        commands have run to do so.
        """
        expected_commands = [
            call(['git', 'fetch', '--all']),
            call(['git', 'checkout', 'origin/master']),
            call(['git', 'checkout', '-b', self.target_branch_name]),
        ]
        for pr in prs:
            expected_commands.append(call(['git', 'merge', 'origin/%s' % pr.branch_name]))
        self.assertListEqual(self.call_in_repo_mock.call_args_list, expected_commands)

    def test_no_prs(self):
        """Runs through the whole process without any PRs being available."""
        with self.activate_mocks():
            prepare_release()
            self.assert_git_commands_ran([])
            self.inspect_and_delete_csv([])

    def test_all_prs_included(self):
        """Runs through the process with a few PRs being available and including all of them."""
        prs = [PullRequestFactory() for i in range(0, 3)]
        self.get_open_prs_patch = patch.object(GitHubRepo, 'get_open_pull_requests', return_value=prs)

        with self.activate_mocks():
            prepare_release()
            self.assert_git_commands_ran(prs)
            self.inspect_and_delete_csv([
                [str(pr.pr_id), str(pr.branch_name)]
                for pr in prs
            ])
