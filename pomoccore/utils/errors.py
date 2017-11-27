# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.


import falcon.status_codes as http_status

from falcon.http_error import HTTPError

from pomoccore.utils import response


class APIError(HTTPError):
    def __init__(self,
                 status,
                 title='We need a title, Ignacio!',
                 description='I told you for the nth time, Ignacio, that we need the error description!',
                 headers=None,
                 code=None):
        super(APIError, self).__init__(
            status=status, title=title, description=description, headers=headers, code=code
        )

    def to_dict(self, obj_type=dict):
        super(APIError, self).to_dict(obj_type)

        obj = obj_type()
        obj['status'] = response.create_response_status_field(
            True, self.status, self.code, self.title, self.description
        )

        return obj


class APIBadRequestError(APIError):
    def __init__(self,
                 title='We need a title, Ignacio!',
                 description='I told you for the nth time, Ignacio, that we need the error message!'):
        super(APIBadRequestError, self).__init__(
            status=http_status.HTTP_400,
            title=title,
            description=description,
            headers=None,
            code='Ignacio, you buffoon! Add a damn internal status code.'
        )


class APIUnauthorizedError(APIError):
    def __init__(self,
                 title='We need a title, Ignacio!',
                 description='I told you for the nth time, Ignacio, that we need the error message!'):
        headers = dict()
        headers['WWW-Authenticate'] = 'Bearer'

        super(APIUnauthorizedError, self).__init__(
            status=http_status.HTTP_401,
            title=title,
            description=description,
            headers=headers,
            code='Ignacio, you buffoon! Add a damn internal status code.'
        )


class APIForbiddenError(APIError):
    def __init__(self,
                 title='We need a title, Ignacio!',
                 description='I told you for the nth time, Ignacio, that we need the error message!'):
        super(APIForbiddenError, self).__init__(
            status=http_status.HTTP_403,
            title=title,
            description=description,
            headers=None,
            code='Ignacio, you buffoon! Add a damn internal status code.'
        )


class APINotFoundError(APIError):
    def __init__(self,
                 title='We need a title, Ignacio!',
                 description='I told you for the nth time, Ignacio, that we need the error message!'):
        super(APINotFoundError, self).__init__(
            status=http_status.HTTP_404,
            title=title,
            description=description,
            headers=None,
            code='Ignacio, you buffoon! Add a damn internal status code.'
        )


class APIConflictError(APIError):
    def __init__(self,
                 title='We need a title, Ignacio!',
                 description='I told you for the nth time, Ignacio, that we need the error message!'):
        super(APIConflictError, self).__init__(
            status=http_status.HTTP_409,
            title=title,
            description=description,
            headers=None,
            code='Ignacio, you buffoon! Add a damn internal status code.'
        )


class APIUnprocessableEntityError(APIError):
    def __init__(self,
                 title='We need a title, Ignacio!',
                 description='I told you for the nth time, Ignacio, that we need the error message!'):
        super(APIUnprocessableEntityError, self).__init__(
            status=http_status.HTTP_422,
            title=title,
            description=description,
            headers=None,
            code='Ignacio, you buffoon! Add a damn internal status code.'
        )
