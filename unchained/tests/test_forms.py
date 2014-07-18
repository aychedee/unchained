# Copyright 2012 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#

from __future__ import unicode_literals

import unittest

from django.contrib.auth.models import User
from django.utils import six

if six.PY3:
    unicode = str

from unchained.forms import RegistrationForm


class RegistrationFormTest(unittest.TestCase):

    def test_clean_raises_if_password_fields_are_not_equal(self):
        form = RegistrationForm(
            dict(
                username='shucks',
                email='valid@example.com',
                password='secret',
                confirm_password='different'
            )
        )
        self.assertEqual(
            ['Passwords do not match'],
            form.non_field_errors()
        )

    def test_clean_raises_if_username_is_already_taken(self):
        User.objects.create(username='double')
        form = RegistrationForm(
            dict(
                username='double',
                email='valid@example.com',
                password='secret',
                confirm_password='secret'
            )
        )
        self.assertEqual(
            ['Sorry, that username is already taken'],
            form.non_field_errors()
        )

    def test_fields_have_correct_attributes(self):
        form = RegistrationForm()

        self.assertEqual(unicode(form.fields['username'].widget.attrs['placeholder']), 'Username')
        self.assertEqual(unicode(form.fields['email'].widget.attrs['placeholder']), 'Email address')
        self.assertEqual(unicode(form.fields['password'].widget.attrs['placeholder']), 'Password')
        self.assertEqual(unicode(form.fields['confirm_password'].widget.attrs['placeholder']), 'Confirm password')
