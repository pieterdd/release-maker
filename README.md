Release Maker
=============

[![Build Status](https://travis-ci.org/pieterdd/release-maker.svg?branch=master)](https://travis-ci.org/pieterdd/release-maker)

Use case
--------

This tool was made for Git release workflows where a batch of pull requests are merged together into a temporary release branch to verify that the build will still pass if merged to master.


Installation and usage
----------------------

You can run `setup.py` in the same way that you would with other Python packages. You can start the release maker by running the `make_release` script. It's actually a symlink to `make_release.py`. For your convenience, you can copy this symlink to a directory in your [environment's path](https://en.wikipedia.org/wiki/PATH_(variable)) so that you can invoke the script from any folder.


What it does
------------

The tool should be run in the root of a Git repository that is hosted on GitHub. When the `make_release` script is invoked, the tool will do the following:

- Ask for a [personal API token](https://github.com/settings/tokens) to authenticate with GitHub.
- Create a temporary release branch originating from the latest `origin/master`. You can choose the branch name.
- One by one, it will go through your open pull requests and ask you which ones need to be merged into the release branch.
- Afterwards, it will offer to write a list of merged branches to a CSV file if you'd like. This can be convenient for internal bookkeeping. As always, you'll also have your Git history.

After the release branch is made, you can manually push your branch to GitHub when you're ready. You may want to run your unit tests, `flake8` or other safety checks in your local environment before you do so.
