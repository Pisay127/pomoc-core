# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.


import json


def http_json_error_serializer(req, resp, exception):
    resp.status = exception.status
    resp.body = json.dumps(exception.to_dict())
    resp.content_type = 'application/json'

    for header, value in exception.headers.items():
        resp.append_header(header, value)

    resp.append_header('Vary', 'Accept')
