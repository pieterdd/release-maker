# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
import factory
from releasemaker.structures import PullRequest, Issue


class IssueFactory(factory.Factory):
    class Meta:
        model = Issue

    issue_id = factory.Sequence(lambda n: n)
    labels = ['Ready']


class PullRequestFactory(factory.Factory):
    class Meta:
        model = PullRequest

    pr_id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: 'Dummy pull request number %d' % n)
    body = 'This is a test'
    branch_name = factory.Sequence(lambda n: 'feature-%d' % n)
    created = factory.LazyAttribute(lambda o: (datetime.now() - timedelta(days=2)).isoformat())
    updated = factory.LazyAttribute(lambda o: datetime.now().isoformat())
    issue = factory.SubFactory(IssueFactory)
