# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models.student import StudentStatus
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class StudentStatusController(object):
    @falcon.before(validators.user.exists)
    def on_get(self, req, resp):
        statuses = db.Session.query(StudentStatus).filter_by(
                        student_id=req.get_json('student_id')
                   ).order_by(StudentStatus.school_year.desc(), StudentStatus.quarter.desc()).all()

        status_ctr = 0
        data = dict()
        data['student'] = dict()
        for status in statuses:
            data['student'][status_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][status_ctr][scope] = getattr(status, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            status_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student statuses retrieval', 'Statuses successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.user.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        status = req.get_json('status').strip()
        quarter = req.get_json('quarter')
        year_level = req.get_json('year_level')
        school_year = req.get_json('school_year')

        db.Session.add(StudentStatus(student_id, status, quarter, year_level, school_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student status successfully', 'New status for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.user.exists)
    def on_put(self, req, resp):
        student_status = db.Session.query(StudentStatus).filter_by(student_id=req.get_json('student_id'),
                                                                   quarter=req.get_json('quarter'),
                                                                   year_level=req.get_json('year_level'),
                                                                   school_year=req.get_json('school_year')
                                                                   ).one()
        student_status.status = req.get_json('status').strip()
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student status updated successfully',
            'Status of student {0} has been updated.'.format(student_status.student_id)
        )

    @falcon.before(validators.user.exists)
    def on_delete(self, req, resp):
        student_status = db.Session.query(StudentStatus).filter_by(student_id=req.get_json('student_id'),
                                                                   quarter=req.get_json('quarter'),
                                                                   year_level=req.get_json('year_level'),
                                                                   school_year=req.get_json('school_year')
                                                                   ).one()
        db.Session.delete(student_status)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student status deleted successfully',
            'Status of student {0} has been deleted.'.format(student_status.student_id)
        )

