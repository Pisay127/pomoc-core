# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.


from pomoccore.modules import falcon_jsonify

from pomoccore.utils.errors import APIBadRequestError


class APIJsonify(falcon_jsonify.Middleware):
    """
    This middleware is just the same as Falcon-Jsonify but with uses the custom HTTP errors (APIError classes)
    of this API so that the response JSONs will be the consistent across all API endpoints.
    """

    def __init__(self):
        super(APIJsonify, self).__init__(True)

    def bad_request(self, title, description):
        raise APIBadRequestError(title=title, description=description)
