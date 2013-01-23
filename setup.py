#!/usr/bin/env python

from distutils.core import setup


setup(
    name='Unchained',
    version='1.01',
    description='Some helper functions for sharing between Django projects',
    author='Hansel Dunlop',
    author_email='hansel@interpretthis.org',
    url='https://github.com/aychedee/unchained',
    packages=['unchained'],
    requires=[
        'django',
    ]

)
