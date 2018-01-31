# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db

from pomoccore.models import StudentCharacterRatingCriteria
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIConflictError


def exists(req, resp, resource, params):
    if req.get_json('criterion_id') == '__all__':  # Denotes that we need all the sections.
        return

    try:
        db.Session.query(StudentCharacterRatingCriteria).filter_by(
            criterion_id=int(req.get_json('criterion_id'))
        ).one()
    except NoResultFound:
        raise APINotFoundError('Criterion could not be found', 'Criterion does not exist, or used to be.')


def name_not_exists(req, resp, resource, params):
    try:
        db.Session.query(StudentCharacterRatingCriteria).filter_by(
            criterion_name=req.get_json('criterion_name')
        ).one()
        raise APIConflictError('Criterion already exists', 'Criterion with the same name already exists.')
    except NoResultFound:
        pass


def not_exists(req, resp, resource, params):
    try:
        db.Session.query(StudentCharacterRatingCriteria).filter_by(
            criterion_id=req.get_json('criterion_id')
        ).one()
        raise APIConflictError('Criterion already exists', 'Criterion already exists.')
    except NoResultFound:
        pass

