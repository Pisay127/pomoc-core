# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import json


def set_successful_response(resp, http_code, app_code, title, description, data=None):
    resp.status = http_code

    response_body = {
        'status': create_response_status_field(False, http_code, app_code, title, description)
    }

    if data is not None:
        response_body['data'] = data

    resp.body = json.dumps(response_body)


def create_response_status_field(is_error, http_code, app_code, title, description):
    return {
        'error': bool(is_error),
        'code': {
            'http': http_code,
            'app': app_code  # This field refers to an internal coding system for errors and successes.
                             # Note: 100 - 799 is reserved for official and unofficial HTTP status codes.
        },
        'title': title,
        'description': description
    }
