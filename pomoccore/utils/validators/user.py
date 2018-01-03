# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore.models import User
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIConflictError


def exists(req, resp, resource, params):
    if req.get_json('user_id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(User).filter_by(user_id=int(req.get_json('user_id'))).one()
    except NoResultFound:
        raise APINotFoundError('User could not be found', 'User does not exist, or used to be.')


def not_exists(req, resp, resource, params):
    try:
        db.Session.query(User).filter_by(user_id=req.get_json('user_id')).one()
        raise APIConflictError('User already exists', 'User with the same username already exists.')
    except NoResultFound:
        pass


def not_exists_by_id_number(req, resp, resource, params):
    try:
        db.Session.query(User).filter_by(id_number=req.get_json('id_number')).one()
        raise APIConflictError('User already exists', 'User with the same username already exists.')
    except NoResultFound:
        pass
