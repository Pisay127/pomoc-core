# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import TeacherPositionList
from pomoccore.utils import validators
from pomoccore.utils import response


class TeacherPositionListController(object):
    @falcon.before(validators.teacher_position_exists)
    def on_get(self, req, resp):
        data = dict()
        data['teacher_position'] = dict()
        if req.get_json('id') == '__all__':
            positions = TeacherPositionList.query.all()

            position_ctr = 0
            for position in positions:
                data['teacher_position'][position_ctr] = {
                    'id': position.position_id,
                    'name': position.position_name
                }

                position_ctr += 1
        else:
            position = db.Session.query(TeacherPositionList).filter_by(position_id=req.get_json('id')).one()

            data['teacher_position'] = {
                'id': position.position_id,
                'name': position.position_name
            }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful teacher position retrieval', 'Teacher position successfully gathered.', data
        )

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.teacher_position_not_exists)
    def on_post(self, req, resp):
        name = req.get_json('name')

        db.Session.add(TeacherPositionList(name))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Teacher position created successfully', 'New position {0} has been created.'.format(name)
        )

    @falcon.before(validators.teacher_position_exists)
    def on_put(self, req, resp):
        position = db.Session.query(TeacherPositionList).filter_by(position_id=req.get_json('id')).one()

        if 'name' in req.json:
            position.position_name = req.get_json('name')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Position updated successfully', 'Position {0} has been updated.'.format(position.position_name)
        )

    @falcon.before(validators.teacher_position_exists)
    def on_delete(self, req, resp):
        position = db.Session.query(TeacherPositionList).filter_by(position_id=req.get_json('id')).one()

        db.Session.delete(position)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Position deleted successfully', 'Position {0} has been deleted.'.format(position.position_name)
        )
