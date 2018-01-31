# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import jwt

from pomoccore import db

from pomoccore import settings
from pomoccore.models import User
from pomoccore.models import Admin
from pomoccore.utils.errors import APIForbiddenError


def username_exists(req, resp, resource, params):
    try:
        user = db.Session.query(User).filter_by(username=req.get_json('admin_username')).one()
        db.Session.query(Admin).filter_by(admin_id=user.user_id).one()
    except NoResultFound:
        raise APINotFoundError('Admin could not be found', 'Admin does not exist, or used to be.')


def exists(req, resp, resource, params):
    if req.get_json('admin_id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(Admin).filter_by(admin_id=int(req.get_json('admin_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Admin could not be found', 'Admin does not exist, or used to be.')


def required(req, resp, resource, params):
    decoded_token = jwt.decode(
        req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
    )

    user_id = int(decoded_token['sub'])
    retrieved_user = db.Session.query(User).filter_by(user_id=user_id).one()

    if retrieved_user.user_type != 'admin':
        raise APIForbiddenError('Forbidden access', 'User must be an admin.')
