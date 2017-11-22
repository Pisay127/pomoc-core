# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import jwt

from jwt import ExpiredSignatureError
from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore import settings
from pomoccore.models import User
from pomoccore.models import Subject
from pomoccore.models.grouping import Section
from pomoccore.models.teacher import TeacherPosition
from pomoccore.models.teacher import TeacherPositionList
from pomoccore.utils.errors import APIBadRequestError
from pomoccore.utils.errors import APINotFoundError
from pomoccore.utils.errors import APIForbiddenError
from pomoccore.utils.errors import APIConflictError


def user_exists(req, resp, resource, params):
    try:
        db.Session.query(User).filter_by(user_id=int(req.get_json('id'))).one()
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

    user_id = int(decoded_token['sub'])

    try:
        db.Session.query(User).filter_by(user_id=user_id).one()
    except NoResultFound:
        raise APINotFoundError('Requesting user non-existent', 'User owning this access token does not exist.')


def user_not_exists(req, resp, resource, params):
    try:
        db.Session.query(User).filter_by(user_id=req.get_json('id')).one()
        raise APIConflictError('User already exists', 'User with the same username already exists.')
    except NoResultFound:
        pass


def admin_required(req, resp, resource, params):
    decoded_token = jwt.decode(
        req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
    )

    user_id = int(decoded_token['sub'])
    retrieved_user = db.Session.query(User).filter_by(user_id=user_id).one()

    if retrieved_user.user_type != 'admin':
        raise APIForbiddenError('Forbidden access', 'User must be an admin.')


def subject_exists(req, resp, resource, params):
    if req.get_json('id') == '__all__':  # Denotes that we need all the subjects.
        return

    try:
        db.Session.query(Subject).filter_by(subject_id=int(req.get_json('id'))).one()
    except NoResultFound:
        raise APINotFoundError('Subject could not be found', 'Subject does not exist, or used to be.')


def subject_not_exists(req, resp, resource, params):
    try:
        db.Session.query(Subject).filter_by(subject_name=req.get_json('name')).one()
        raise APIConflictError('Subject already exists', 'Subject with the same name already exists.')
    except NoResultFound:
        pass


def section_exists(req, resp, resource, params):
    if req.get_json('id') == '__all__':  # Denotes that we need all the sections.
        return

    try:
        db.Session.query(Section).filter_by(section_id=int(req.get_json('id'))).one()
    except NoResultFound:
        raise APINotFoundError('Section could not be found', 'Section does not exist, or used to be.')


def section_not_exists(req, resp, resource, params):
    try:
        db.Session.query(Section).filter_by(section_name=req.get_json('name')).one()
        raise APIConflictError('Section already exists', 'Section with the same name already exists.')
    except NoResultFound:
        pass


def teacher_position_exists_2(req, resp, resource, params):
    try:
        db.Session.query(TeacherPosition).filter_by(position_id=int(req.get_json('position_id'))).one()
    except NoResultFound:
        raise APINotFoundError('Teacher position could not be found', 'Position does not exist, or used to be.')


def teacher_position_exists(req, resp, resource, params):
    if req.get_json('id') == '__all__':  # Denotes that we need all the teacher positions
        return

    try:
        db.Session.query(TeacherPositionList).filter_by(position_id=int(req.get_json('id'))).one()
    except NoResultFound:
        raise APINotFoundError('Teacher could not be found', 'Section does not exist, or used to be.')


def teacher_position_not_exists(req, resp, resource, params):
    try:
        db.Session.query(TeacherPositionList).filter_by(position_id=int(req.get_json('id'))).one()
        raise APIConflictError('Teacher position already exists', 'Position with the same name already exists.')
    except NoResultFound:
        pass
