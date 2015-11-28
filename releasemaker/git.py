# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import subprocess
from releasemaker.exceptions import MergeFailure, InvalidRemote


class GitInterface(object):
    """
    Takes care of the interaction with the Git repository.
    """
    def __init__(self, repo_dir, remote='origin', master_branch='master'):
        self.repo_dir = repo_dir
        self.remote = remote
        self.master_branch = master_branch

    @classmethod
    def create_from_cwd(cls):
        """Creates a GitInterface object from the Git repo in the current working directory."""
        cwd = os.getcwd()
        return GitInterface(cwd)

    def infer_repo_details(self):
        """Extract the owner and name of the Git repository. Both are returned as a tuple."""
        remote_url = self.check_output_in_repo_dir(['git', 'config', '--get', 'remote.origin.url'])
        remote_matcher = re.search(r':([^\/]+)/([^\.]+)\.git$', remote_url)
        if not remote_matcher:
            raise InvalidRemote(remote_url)

        # Returns the owner first, then the repo name
        return remote_matcher.group(1), remote_matcher.group(2)

    @property
    def remote_master_branch(self):
        """Returns full name of remote master branch."""
        return '%s/%s' % (self.remote, self.master_branch)

    def call_in_repo_dir(self, call_arg_list, assert_success=True):
        """
        Performs a call in the repo directory.

        :param assert_success:
                If True, will raise exception if the call was unsuccessful.
        """
        if assert_success:
            return subprocess.check_call(call_arg_list, cwd=self.repo_dir)
        else:
            return subprocess.call(call_arg_list, cwd=self.repo_dir)

    def check_output_in_repo_dir(self, call_arg_list):
        """Returns output of a call in the repo directory."""
        return subprocess.check_output(call_arg_list, cwd=self.repo_dir)

    def fetch_all(self):
        """Collects new objects and references from the default remote."""
        self.call_in_repo_dir(['git', 'fetch', '--all'])

    def tracked_files_changed(self):
        """
        If the repo contains changes in tracked files (either staged or unstaged), this will return True.
        """

        # Check for unstaged changes. They may interfere with branch switching.
        if self.check_output_in_repo_dir(['git', 'diff']) != '':
            return True
        # Now check for staged changes. They might trigger avoidable merge conflicts when building a release branch.
        elif self.check_output_in_repo_dir(['git', 'diff', '--staged']) != '':
            return True
        return False

    def create_release_branch(self, branch_name):
        """
        Starting from the remote's master branch, we'll create a fresh release branch.

        :param branch_name:
                What to call the release branch.
        """
        self.call_in_repo_dir(['git', 'checkout', self.remote_master_branch])
        self.call_in_repo_dir(['git', 'checkout', '-b', branch_name])

    def merge_branch(self, branch_to_merge):
        """Merges a given branch into the current branch. Don't prefix with the remote name!"""
        try:
            self.call_in_repo_dir(['git', 'merge', '%s/%s' % (self.remote, branch_to_merge)])
        except subprocess.CalledProcessError:
            raise MergeFailure(branch_to_merge)
