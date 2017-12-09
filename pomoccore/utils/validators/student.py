# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore.models import Student
from pomoccore.utils.errors import APINotFoundError


def exists(req, resp, resource, params):
    if req.get_json('student_id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(Student).filter_by(student_id=int(req.get_json('student_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Student could not be found', 'student does not exist, or used to be.')
