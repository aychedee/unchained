# Copyright 2013 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#

from django.template import Context
from django.template.loader import get_template

from mock import call, patch, Mock

from common import send_html_email
from tests.npsxtest import NPSXTestCase



class SendHtmlEmailTest(NPSXTestCase):

    @patch('common.EmailMultiAlternatives')
    def test_renders_to_correct_templates_and_then_delegates(self, mockEmail):

        subject = 'I am subject'
        sender = 'o@no.com'
        recipients = ['a@duh.com']
        msg = Mock()
        mockEmail.return_value = msg
        email_context = {'some': 'random context'}

        send_html_email(
            subject, 'confirm_email', sender, recipients, email_context
        )

        email_txt = get_template('confirm_email.txt').render(Context(email_context))
        email_html = get_template('confirm_email.html').render(Context(email_context))

        self.assertEqual(msg.attach_alternative.call_args_list,
            [call(email_html, 'text/html')]
        )

        self.assertEqual(mockEmail.call_args_list,
            [call(subject, email_txt, sender, recipients)]
        )

