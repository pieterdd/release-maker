# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from contextlib import contextmanager
import csv
import os
from unittest import TestCase
from releasemaker.cli_io import prepare_release
from releasemaker.api import GitHubRepo
from releasemaker.git import GitInterface
from mock import patch


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
        self.ask_export_csv = patch('releasemaker.cli_io.ask_export_csv', return_value=True)

    @contextmanager
    def activate_mocks(self):
        with self.ask_token_patch, self.infer_repo_details_patch, self.tracked_file_patch, self.call_in_repo_patch,\
              self.check_output_in_repo_patch, self.ask_target_branch_patch, self.ask_filter_labels_patch,\
              self.get_open_prs_patch, self.ask_export_csv:
            yield

    def inspect_and_delete_csv(self, csv_file_name, expected_rows):
        """
        Ensure the contents of a CSV file to see if the contents align with the expected values. Then removes it from
        disk to avoid unit test leftovers.
        """
        with open(csv_file_name, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            actual_rows = list(csv_reader)
            self.assertListEqual(actual_rows, expected_rows)
        os.remove(csv_file_name)

    def test_no_prs(self):
        """Runs through the whole process without any PRs being available."""
        with self.activate_mocks():
            prepare_release()
            self.inspect_and_delete_csv('%s.csv' % self.target_branch_name, [])
