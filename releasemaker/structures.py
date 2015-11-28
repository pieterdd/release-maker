# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from dateutil import parser


class PullRequest(object):
    """Contains the state of a pull request on GitHub."""
    def __init__(self, pr_id, title, body, branch_name, created, updated, issue=None):
        self.pr_id = pr_id
        self.title = title
        self.body = body
        self.branch_name = branch_name
        self.created = parser.parse(created)
        self.updated = parser.parse(updated)
        self.issue = issue

    def __str__(self):
        return self.title

    def unicode_multiline(self):
        """A multiline unicode representation of this pull request."""
        multiline = [
            '#%d: %s' % (self.pr_id, self.title),
            self.branch_name,
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
