# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models.student import StudentStatus
from pomoccore.utils import validators
from pomoccore.utils import response


class StudentStatusController(object):
    @falcon.before(validators.student_exists)
    def on_get(self, req, resp):
        statuses = db.Session.query(StudentStatus).filter_by(
                        student_id=req.get_json('id')
                   ).order_by(StudentStatus.school_year.desc(), StudentStatus.quarter.desc()).all()

        row_ctr = 0
        data = dict()
        data['student'] = dict()
        for status in statuses:
            data['student'][row_ctr] = {
                'id': status.student_id,
                'status': status.status,
                'quarter': status.quarter,
                'year_level': status.year_level,
                'school_year': status.school_year
            }

            row_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student statuses retrieval', 'Statuses successfully gathered.', data
        )

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.user_exists)
    def on_post(self, req, resp):
        id_number = req.get_json('id')
        status = req.get_json('status').strip()
        quarter = req.get_json('quarter')
        year_level = req.get_json('year_level')
        school_year = req.get_json('school_year')

        db.Session.add(StudentStatus(id_number, status, quarter, year_level, school_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student status successfully', 'New status for {0} has been added.'.format(id_number)
        )

    @falcon.before(validators.user_exists)
    def on_put(self, req, resp):
        student_status = db.Session.query(StudentStatus).filter_by(student_id=req.get_json('id'),
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

    @falcon.before(validators.user_exists)
    def on_delete(self, req, resp):
        student_status = db.Session.query(StudentStatus).filter_by(student_id=req.get_json('id'),
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

