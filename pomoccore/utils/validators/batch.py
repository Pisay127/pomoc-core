# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore.models import Batch
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIConflictError


def exists(req, resp, resource, params):
    if req.get_json('batch_year') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(Batch).filter_by(batch_year=int(req.get_json('batch_year'))).one()
    except NoResultFound:
        raise APINotFoundError('Batch year could not be found', 'Batch year does not exist, or used to be.')


def not_exists(req, resp, resource, params):
    try:
        db.Session.query(Batch).filter_by(batch_year=req.get_json('batch_year')).one()
        raise APIConflictError('Batch year already exists', 'Batch year already exists.')
    except NoResultFound:
        pass
