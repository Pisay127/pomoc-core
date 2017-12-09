# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from pomoccore.utils import misc


class ScopeRetrieval(object):
    def process_request(self, req, resp):
        if not req.content_length:
            return

        req.scope = misc.get_requested_scope(req.get_json('scope'))

    def process_response(self, req, resp, resource, req_succeeded):
        pass
