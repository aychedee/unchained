# Copyright 2013 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#

class ReferrerMiddleware(object):

    def process_request(self, request):
        if 'referrer' not in request.session:
            request.session['referrer'] = request.META.get('HTTP_REFERER', '')
