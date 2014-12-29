#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2012 Ilya Shalyapin
#
#  django-resized is free software under terms of the MIT License.
#

import os
from setuptools import setup, find_packages


setup(
    name     = 'django-resized',
    version  = '0.2.4',
    packages = find_packages(),
    requires = ['python (>= 2.5)', 'django (>= 1.0)'],
    description  = 'Deletes old files.',
    long_description = open('README.markdown').read(),
    author       = 'Ilya Shalyapin',
    author_email = 'ishalyapin@gmail.com',
    url          = 'https://github.com/un1t/django-resized',
    download_url = 'https://github.com/un1t/django-resized/tarball/master',
    license      = 'MIT License',
    keywords     = 'django',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
