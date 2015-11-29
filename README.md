Release Maker
=============

[![Build Status](https://travis-ci.org/pieterdd/release-maker.svg?branch=feature%2Ftravis-build)](https://travis-ci.org/pieterdd/release-maker)

Use case
--------

This tool was made for Git release workflows where a batch of pull requests are merged together into a temporary release branch to verify that the build will still pass if merged to master.


Installation
------------

You can run `setup.py` in the same way that you would with other Python packages. For your convenience, we've included a `prepare_release` symlink. If this symlink is reachable from your [environment's path](https://en.wikipedia.org/wiki/PATH_(variable)) (or copied into a directory that's in your path), you can invoke it from any folder by calling `prepare_release`.


How it works
------------

The tool should be run in the root of a Git repository that is hosted on GitHub. When invoking the `prepare_release.py` script, the tool will do the following:

- Ask for a [personal API token](https://github.com/settings/tokens) to authenticate with GitHub.
- Create a temporary release branch originating from the latest `origin/master`. You can choose the branch name.
- One by one, it will go through your open pull requests and ask you which ones need to be merged into the release branch.
- Afterwards, it will offer to write a list of merged branches to a CSV file if you'd like. This can be convenient for internal bookkeeping. As always, you'll also have your Git history.
