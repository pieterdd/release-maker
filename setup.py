#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup

setup(
    name='Release Maker',
    version='0.1',
    description='Python tool to combine open GitHub pull requests into a release branch',
    author='Pieter De Decker',
    install_requires=[
        'setuptools>=17.1',
        'requests>=2.8.1',
        'python-dateutil>=2.4.2',
        'mock>=1.3.0',
        'factory-boy>=2.6.0',
    ]
)
