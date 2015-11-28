# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


class ResourceNotFound(Exception):
    """Raised when encountering HTTP 404 during a call to the GitHub API"""
    pass


class MergeFailure(Exception):
    """Raised when a Git merge failed."""
    def __init__(self, branch_name):
        super(MergeFailure, self).__init__('Branch %s could not be merged' % branch_name)
        self.branch_name = branch_name


class InvalidRemote(Exception):
    """Raised when Git remote URL doesn't follow the expected format, e.g. when not connected over SSH."""
    def __init__(self, remote_url):
        super(InvalidRemote, self).__init__('Format of remote %s is not recognized.' % remote_url)
        self.remote_url = remote_url
