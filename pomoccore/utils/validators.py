# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import jwt

from jwt import ExpiredSignatureError
from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore import settings
from pomoccore.models import User
from pomoccore.utils.errors import APIBadRequestError
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIForbiddenError
from pomoccore.utils.errors import APIConflictError


def user_exists(req, resp, resource, params):
    try:
        db.Session.query(User).filter_by(username=req.get_json('username')).one()
    except NoResultFound:
        raise APINotFoundError('User could not be found', 'User does not exist, or used to be.')


def validate_access_token(req, resp, resource, params):
    if 'access_token' not in req.json:
        raise APIForbiddenError('Forbidden access', 'No access token found.')

    try:
        jwt.decode(
            req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
        )
    except ExpiredSignatureError:
        raise APIBadRequestError('Expired access token', 'The access token has expired,')


def access_token_requesting_user_exists(req, resp, resource, params):
    decoded_token = jwt.decode(
        req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
    )

    username=decoded_token['sub']

    try:
        db.Session.query(User).filter_by(username=username).one()
    except NoResultFound:
        raise APINotFoundError('Requesting user non-existent', 'User owning this access token does not exist.')


def user_already_exists(req, resp, resource, params):
    try:
        db.Session.query(User).filter_by(username=req.get_json('username')).one()
        raise APIConflictError('User already exists', 'User with the same username already exists.')
    except NoResultFound:
        pass


def admin_required(req, resp, resource, params):
    decoded_token = jwt.decode(
        req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
    )

    username = decoded_token['sub']
    retrieved_user = db.Session.query(User).filter_by(username=username).one()

    if retrieved_user.user_type != 'admin':
        raise APIForbiddenError('Forbidden access', 'User must be an admin.')
