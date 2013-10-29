# Copyright 2013 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#

from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
import unittest

from unchained.middleware import ReferrerMiddleware


class RefererMiddlewareTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        SessionMiddleware().process_request(self.request)

    def test_process_request_saves_referrer_for_life_of_session(self):

        rmw = ReferrerMiddleware()

        self.request.META['HTTP_REFERER'] = 'the queen'
        rmw.process_request(self.request)
        self.assertEqual('the queen', self.request.session['referrer'])

        self.request.META['HTTP_REFERER'] = 'not a queen'
        rmw.process_request(self.request)
        self.assertEqual('the queen', self.request.session['referrer'])


    def test_process_request_handles_blank_referrer(self):

        rmw = ReferrerMiddleware()

        rmw.process_request(self.request)
        self.assertEqual('', self.request.session['referrer'])

    def test_process_request_overwrites_empty_string_referrer(self):

        rmw = ReferrerMiddleware()

        self.request.META['HTTP_REFERER'] = ''
        rmw.process_request(self.request)
        self.assertEqual('', self.request.session['referrer'])

        self.request.META['HTTP_REFERER'] = 'internal link'
        rmw.process_request(self.request)
        self.assertEqual('internal link', self.request.session['referrer'])
