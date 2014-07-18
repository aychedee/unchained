#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.core import Command
from os import path

SITE_ROOT = path.dirname(path.realpath(__file__))


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=(
                'unchained',
                'django.contrib.auth',
                'django.contrib.contenttypes'
            ),
            TEMPLATE_DIRS=(
                path.join(SITE_ROOT, 'unchained/tests/templates')
            )
        )
        from django.core.management import call_command
        import django

        if django.VERSION[:2] >= (1, 7):
            django.setup()
            django.setup()
        call_command('syncdb', interactive=False, verbosity=0)
        call_command('test', 'unchained')


setup(name='unchained',
    version='1.1',
    packages=['unchained'],
    license='MIT',
    author='Hansel Dunlop',
    author_email='hansel@interpretthis.org',
    url='https://github.com/aychedee/unchained/',
    description='A collection of helper functions that helps Django break free',
    long_description=open("README.md").read(),
    install_requires=['Django >= 1.4.3'],
    tests_require=['Django >= 1.4.3'],
    cmdclass={'test': TestCommand},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
)
