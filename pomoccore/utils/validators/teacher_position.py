# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore.models import TeacherPositionList
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIConflictError


def exists(req, resp, resource, params):
    if req.get_json('teacher_position_id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(TeacherPositionList).filter_by(position_id=int(req.get_json('teacher_position_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Teacher could not be found', 'Teacher does not exist, or used to be.')


def not_exists(req, resp, resource, params):
    try:
        db.Session.query(TeacherPositionList).filter_by(position_id=int(req.get_json('teacher_position_id'))).one()
        raise APIConflictError('Position already exists', 'Same position already exists.')
    except NoResultFound:
        pass
