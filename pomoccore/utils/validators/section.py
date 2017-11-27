# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db

from pomoccore.models.grouping import Section
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIConflictError


def exists(req, resp, resource, params):
    if req.get_json('section_id') == '__all__':  # Denotes that we need all the sections.
        return

    try:
        db.Session.query(Section).filter_by(section_id=int(req.get_json('section_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Section could not be found', 'Section does not exist, or used to be.')


def not_exists(req, resp, resource, params):
    try:
        db.Session.query(Section).filter_by(section_name=req.get_json('section_name')).one()
        raise APIConflictError('Section already exists', 'Section with the same name already exists.')
    except NoResultFound:
        pass
