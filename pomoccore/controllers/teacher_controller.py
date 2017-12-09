# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import User
from pomoccore.models import Teacher
from pomoccore.models import TeacherPosition
from pomoccore.models import TeacherPositionList
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class TeacherController(object):
    @falcon.before(validators.teacher.exists)
    def on_get(self, req, resp):
        data = dict()
        data['teacher'] = dict()
        if req.get_json('id') == '__all__':
            teachers = User.query.filter_by(user_type='teacher').all().order_by(User.last_name.asc(),
                                                                                User.first_name.asc(),
                                                                                User.middle_name.asc(),
                                                                                User.id_number.asc())

            teacher_ctr = 0
            for teacher in teachers:
                data['teacher'][teacher_ctr] = {
                    'teacher_id': teacher.user_id
                }

                teacher_ctr += 1
        else:
            teacher = db.Session.query(Teacher).filter_by(teacher_id=req.get_json('teacher_id')).one()

            data['teacher'] = {
                'teacher_id': teacher.teacher_id
            }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful teacher data retrieval', 'Teacher data successfully gathered.', data
        )


class TeacherPositionController(object):
    @falcon.before(validators.teacher.exists)
    def on_get(self, req, resp):
        positions = db.Session.query(TeacherPosition).filter_by(
                       teacher_id=req.get_json('teacher_id')
                    ).order_by(TeacherPosition.school_year.desc(), TeacherPosition.date_created.desc()).all()

        position_ctr = 0
        data = dict()
        data['teacher'] = dict()
        for position in positions:
            data['teacher'][position_ctr] = dict()

            for scope in req.scope:
                try:
                    data['teacher'][position_ctr][scope] = getattr(position, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            position_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful teacher positions retrieval', 'Teacher positions successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.teacher.exists)
    @falcon.before(validators.teacher_position.exists)
    def on_post(self, req, resp):
        teacher_id = req.get_json('teacher_id')
        position_id = req.get_json('teacher_position_id')
        school_year = req.get_json('school_year')

        db.Session.add(TeacherPosition(teacher_id, position_id, school_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Teacher position created successfully', 'New position {0} has been created.'.format(position_id)
        )

    @falcon.before(validators.teacher.exists)
    def on_put(self, req, resp):
        position = db.Session.query(TeacherPosition).filter_by(teacher_id=req.get_json('teacher_id')).one()

        for attrib in req.json:
            setattr(position, attrib, req.get_json(attrib))

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Teacher position updated successfully', 'Position {0} has been updated.'.format(position.position_id)
        )

    @falcon.before(validators.user.exists)
    @falcon.before(validators.teacher_position.exists)
    def on_delete(self, req, resp):
        position = db.Session.query(TeacherPosition).filter_by(teacher_id=req.get_json('teacher_id'),
                                                               position_id=req.get_json('teacher_position_id'),
                                                               school_year=req.get_json('school_year')).one()

        db.Session.delete(position)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Position deleted successfully', 'Position {0} has been deleted.'.format(position.position_name)
        )


class TeacherPositionListController(object):
    @falcon.before(validators.teacher_position.exists)
    def on_get(self, req, resp):
        data = dict()
        data['teacher_position'] = dict()
        if req.get_json('teacher_position_id') == '__all__':
            positions = TeacherPositionList.query.all()

            position_ctr = 0
            for position in positions:
                data['teacher_position'][position_ctr] = dict()
                for scope in req.scope:
                    try:
                        data['teacher_position'][position_ctr][scope] = getattr(position, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the user.')

                position_ctr += 1
        else:
            position = db.Session.query(TeacherPositionList).filter_by(position_id=req.get_json('id')).one()

            data['teacher_position'] = dict()
            for scope in req.scope:
                try:
                    data['teacher_position'][scope] = getattr(position, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful teacher position retrieval', 'Teacher position successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.teacher_position.not_exists)
    def on_post(self, req, resp):
        name = req.get_json('position_name')

        db.Session.add(TeacherPositionList(name))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Teacher position created successfully', 'New position {0} has been created.'.format(name)
        )

    @falcon.before(validators.teacher_position.exists)
    def on_put(self, req, resp):
        position = db.Session.query(TeacherPositionList)\
                             .filter_by(position_id=req.get_json('teacher_position_id')).one()

        for attrib in req.json:
            setattr(position, attrib, req.get_json(attrib))

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Position updated successfully', 'Position {0} has been updated.'.format(position.position_name)
        )

    @falcon.before(validators.teacher_position.exists)
    def on_delete(self, req, resp):
        position = db.Session.query(TeacherPositionList)\
                             .filter_by(position_id=req.get_json('teacher_position_id')).one()

        db.Session.delete(position)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Position deleted successfully', 'Position {0} has been deleted.'.format(position.position_name)
        )
