# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db

from pomoccore.models import Subject
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIConflictError


def exists(req, resp, resource, params):
    if req.get_json('subject_id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(Subject).filter_by(subject_id=int(req.get_json('subject_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Subject could not be found', 'Subject does not exist, or used to be.')


def not_exists(req, resp, resource, params):
    try:
        db.Session.query(Subject).filter_by(subject_name=req.get_json('subject_name')).one()
        raise APIConflictError('Subject already exists', 'Subject with the same name already exists.')
    except NoResultFound:
        pass
