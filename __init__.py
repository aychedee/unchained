# Copyright 2012 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


def send_html_email(subject, template_stub, sender, recipients, context):
    email_txt = get_template(template_stub + '.txt').render(Context(context))
    email_html = get_template(template_stub + '.html').render(Context(context))
    msg = EmailMultiAlternatives(subject, email_txt, sender, recipients)
    msg.attach_alternative(email_html, "text/html")
    msg.send()

