# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import jwt

from jwt import ExpiredSignatureError

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore import settings
from pomoccore.models import User
from pomoccore.utils.errors import APIBadRequestError
from pomoccore.utils.errors import APIForbiddenError
from pomoccore.utils.errors import APINotFoundError


def access_token_valid(req, resp, resource, params):
    if 'access_token' not in req.json:
        raise APIForbiddenError('Forbidden access', 'No access token found.')

    try:
        jwt.decode(
            req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
        )
    except ExpiredSignatureError:
        raise APIBadRequestError('Expired access token', 'The access token has expired,')


def access_token_user_exists(req, resp, resource, params):
    decoded_token = jwt.decode(
        req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
    )

    user_id = int(decoded_token['sub'])

    try:
        db.Session.query(User).filter_by(user_id=user_id).one()
    except NoResultFound:
        raise APINotFoundError('Requesting user non-existent', 'User owning this access token does not exist.')
