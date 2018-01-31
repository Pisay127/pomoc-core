# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import jwt

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore import settings
from pomoccore.models import Teacher
from pomoccore.models import User
from pomoccore.utils.errors import APIForbiddenError
from pomoccore.utils.errors import APINotFoundError


def exists(req, resp, resource, params):
    if req.get_json('teacher_id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(Teacher).filter_by(teacher_id=int(req.get_json('teacher_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Teacher could not be found', 'Teacher does not exist, or used to be.')


def new_exists(req, resp, resource, params):
    if req.get_json('new_teacher_id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(Teacher).filter_by(teacher_id=int(req.get_json('new_teacher_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Teacher could not be found', 'Teacher does not exist, or used to be.')


def required(req, resp, resource, params):
    decoded_token = jwt.decode(
        req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
    )

    user_id = int(decoded_token['sub'])
    retrieved_user = db.Session.query(User).filter_by(user_id=user_id).one()

    if retrieved_user.user_type != 'teacher':
        raise APIForbiddenError('Forbidden access', 'User must be an teacher.')
