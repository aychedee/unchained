# Copyright 2013 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#

from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import get_template
from mock import call, patch, Mock
import unittest

from unchained import format_cents, send_html_email, UsernameOrEmailBackend


class SendHtmlEmailTest(unittest.TestCase):

    html_template = 'confirm_email.html'
    txt_template = 'confirm_email.txt'

    @patch('unchained.EmailMultiAlternatives')
    def test_renders_to_correct_templates_and_then_delegates(
            self, mockEmail
    ):

        subject = 'I am subject'
        sender = 'o@no.com'
        recipients = ['a@duh.com']
        msg = Mock()
        mockEmail.return_value = msg
        email_context = {'some': 'random context'}

        send_html_email(
            subject, 'confirm_email', sender, recipients, email_context
        )

        email_txt = get_template(self.txt_template).render(Context(email_context))
        email_html = get_template(self.html_template).render(Context(email_context))

        self.assertEqual(msg.attach_alternative.call_args_list,
            [call(email_html, 'text/html')]
        )

        self.assertEqual(mockEmail.call_args_list,
            [call(subject, email_txt, sender, recipients)]
        )


class FormatCentsTest(unittest.TestCase):

    def test_format_cents(self):

        for ii in range(90088, 100099):
            result = format_cents(ii)

            expected = '{:,.2f}'.format(ii / 100.0)
            self.assertEqual(expected, result)


class AuthenticationBackendTest(unittest.TestCase):

    def test_authenticate_accepts_emails_or_usernames(self):
        user = User(username='OMG', email='OMG@WHAT.com')
        user.set_password('secret')
        user.save()

        backend = UsernameOrEmailBackend()

        self.assertEqual(
            backend.authenticate(username='OMG', password='secret'),
            user,
        )
        self.assertEqual(
            backend.authenticate(username='OMG@WHAT.com', password='secret'),
            user,
        )
        self.assertEqual(
            backend.authenticate(username='ZOMG@WHAT.com', password='secret'),
            None,
        )
        self.assertEqual(
            backend.authenticate(username='OMG@WHAT.com', password='ssecret'),
            None,
        )
