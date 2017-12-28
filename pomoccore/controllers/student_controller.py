# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Student
from pomoccore.models import StudentSection
from pomoccore.models import StudentBatch
from pomoccore.models import StudentGWA
from pomoccore.models import StudentCharacterRatingCriteria
from pomoccore.models import StudentMonthlyRequiredDays
from pomoccore.models import StudentMonthlyAttendance
from pomoccore.models import StudentRating
from pomoccore.models import StudentStatus
from pomoccore.models import StudentSubject
from pomoccore.models import StudentSubjectGrade
from pomoccore.models import StudentSubjectPendingGrade
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class StudentController(object):
    @falcon.before(validators.student.exists)
    def on_get(self, req, resp):
        data = dict()
        data['student'] = dict()
        if req.get_json('student_id') == '__all__':
            students = Student.query.all()

            row_ctr = 0
            for student in students:
                data['student'][row_ctr] = dict()

                for scope in req.scope:
                    try:
                        data['student'][row_ctr][scope] = getattr(student, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the student.')

                row_ctr += 1
        else:
            student = db.Session.query(Student).filter_by(student_id=req.get_json('student_id')).one()

            data['student'] = dict()
            for scope in req.scope:
                try:
                    data['student'][scope] = getattr(student, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the student.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student data retrieval', 'Student data successfully gathered.', data
        )


class StudentSectionController(object):
    @falcon.before(validators.student.exists)
    def on_get(self, req, resp):
        sections = db.Session.query(StudentSection).filter_by(
                                    student_id=req.get_json('student_id')
                                   ).order_by(StudentSection.school_year.desc()).all()

        section_ctr = 0
        data = dict()
        data['student'] = dict()
        for section in sections:
            data['student'][section_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][section_ctr][scope] = getattr(section, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            section_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student sections retrieval', 'Sections successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.student.exists)
    @falcon.before(validators.section.not_exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        section_id = req.get_json('section_id')
        school_year = req.get_json('school_year')

        db.Session.add(StudentSection(student_id, section_id, school_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student section successfully', 'New section for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    @falcon.before(validators.section.exists)
    def on_put(self, req, resp):
        student_section = db.Session.query(StudentSection).filter_by(student_id=req.get_json('student_id'),
                                                                     section_id=req.get_json('section_id'),
                                                                     school_year=req.get_json('school_year')
                                                                     ).one()

        if 'section_id' in req.json:
            student_section.section_id = req.get_json('section_id')

        if 'school_year' in req.json:
            student_section.school_year = req.get_json('school_year')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student section updated successfully',
            'Section of student {0} has been updated.'.format(student_section.student_id)
        )

    @falcon.before(validators.student.exists)
    @falcon.before(validators.section.exists)
    def on_delete(self, req, resp):
        student_section = db.Session.query(StudentSection).filter_by(student_id=req.get_json('student_id'),
                                                                     section_id=req.get_json('section_id'),
                                                                     school_year=req.get_json('school_year')
                                                                     ).one()
        db.Session.delete(student_section)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student status deleted successfully',
            'Status of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentGWAController(object):
    @falcon.before(validators.student.exists)
    def on_get(self, req, resp):
        gwas = db.Session.query(StudentGWA).filter_by(student_id=req.get_json('student_id')
                                                      ).order_by(StudentGWA.school_year.desc(),
                                                                 StudentGWA.quarter.asc()
                                                                 ).all()

        row_ctr = 0
        data = dict()
        data['student'] = dict()
        for gwa in gwas:
            data['student'][row_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][row_ctr][scope] = getattr(gwa, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the student GWA.')

            row_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student sections retrieval', 'Sections successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.student.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        gwa = req.get_json('gwa')
        quarter = req.get_json('quarter')
        school_year = req.get_json('school_year')

        db.Session.add(StudentGWA(student_id, gwa, quarter, school_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student GWA successfully', 'New GWA for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    def on_put(self, req, resp):
        student_gwa = db.Session.query(StudentGWA).filter_by(student_id=req.get_json('student_id'),
                                                             quarter=req.get_json('quarter'),
                                                             school_year=req.get_json('school_year')
                                                             ).one()

        if 'gwa' in req.json:
            student_gwa.gwa = req.get_json('gwa')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student GWA updated successfully',
            'GWA of student {0} has been updated.'.format(student_gwa.student_id)
        )

    @falcon.before(validators.student.exists)
    def on_delete(self, req, resp):
        student_gwa = db.Session.query(StudentGWA).filter_by(student_id=req.get_json('student_id'),
                                                             quarter=req.get_json('quarter'),
                                                             school_year=req.get_json('school_year')
                                                             ).one()
        db.Session.delete(student_gwa)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student GWA deleted successfully',
            'GWA of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentRatingController(object):
    @falcon.before(validators.student.exists)
    def on_get(self, req, resp):
        ratings = db.Session.query(StudentRating).filter_by(student_id=req.get_json('student_id')
                                                            ).order_by(StudentRating.school_year.desc(),
                                                                       StudentRating.quarter.asc()
                                                                       ).all()

        row_ctr = 0
        data = dict()
        data['student'] = dict()
        for rating in ratings:
            data['student'][row_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][row_ctr][scope] = getattr(rating, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the student rating.')

            row_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student ratings retrieval', 'Ratings successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.student.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        criterion_id = req.get_json('criterion_id')
        rating = req.get_json('rating')
        quarter = req.get_json('quarter')
        year_level = req.get_json('year_level')
        school_year = req.get_json('school_year')

        db.Session.add(StudentRating(student_id, criterion_id, rating, quarter, year_level, school_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student rating successfully', 'New rating for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    @falcon.before(validators.rating_criteria.exists)
    def on_put(self, req, resp):
        student_rating = db.Session.query(StudentRating).filter_by(student_id=req.get_json('student_id'),
                                                                   criterion_id=req.get_json('criterion_id'),
                                                                   quarter=req.get_json('quarter'),
                                                                   year_level=req.get_json('year_level'),
                                                                   school_year=req.get_json('school_year')
                                                                   ).one()

        if 'rating' in req.json:
            student_rating.rating = req.get_json('rating')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student rating updated successfully',
            'Rating of student {0} has been updated.'.format(student_rating.student_id)
        )

    @falcon.before(validators.student.exists)
    def on_delete(self, req, resp):
        student_rating = db.Session.query(StudentRating).filter_by(student_id=req.get_json('student_id'),
                                                                   criterion_id=req.get_json('criterion_id'),
                                                                   quarter=req.get_json('quarter'),
                                                                   year_level=req.get_json('year_level'),
                                                                   school_year=req.get_json('school_year')
                                                                   ).one()
        db.Session.delete(student_rating)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student rating deleted successfully',
            'rating of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentRatingCriteriaController(object):
    @falcon.before(validators.rating_criteria.exists)
    def on_get(self, req, resp):
        data = dict()
        data['rating_criteria'] = dict()
        if req.get_json('criterion_id') == '__all__':
            criteria = StudentCharacterRatingCriteria.query.all()

            row_ctr = 0
            for criterion in criteria:
                data['rating_criteria'][row_ctr] = dict()

                for scope in req.scope:
                    try:
                        data['rating_criteria'][row_ctr][scope] = getattr(criterion, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the rating criteria.')

                row_ctr += 1
        else:
            criterion = db.Session.query(StudentCharacterRatingCriteria).filter_by(
                criterion_id=req.get_json('criterion_id')
            ).one()

            data['rating_criteria'] = dict()
            for scope in req.scope:
                try:
                    data['rating_criteria'][scope] = getattr(criterion, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the criteria.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful rating criteria retrieval', 'Rating criteria successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.rating_criteria.not_exists)
    def on_post(self, req, resp):
        criterion_id = req.get_json('criterion_id')
        criterion_description = req.get_json('criterion_description')

        db.Session.add(StudentCharacterRatingCriteria(criterion_id, criterion_description))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new criterion successfully', 'New criterion for {0} has been added.'.format(criterion_id)
        )

    @falcon.before(validators.rating_criteria.exists)
    def on_put(self, req, resp):
        criterion = db.Session.query(StudentCharacterRatingCriteria).filter_by(
            criterion_id=req.get_json('criterion_id')
        ).one()

        if 'criterion_description' in req.json:
            criterion.criterion_description = req.get_json('criterion_description')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Criterion updated successfully',
            'Criterion has been updated.'.format(criterion.criterion_id)
        )

    @falcon.before(validators.rating_criteria.exists)
    def on_delete(self, req, resp):
        criterion = db.Session.query(StudentCharacterRatingCriteria).filter_by(
            criterion_id=req.get_json('criterion_id')
        ).one()

        db.Session.delete(criterion)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Criterion deleted successfully',
            'Criterion has been deleted.'.format(req.get_json('student_id'))
        )


class StudentBatchController(object):
    @falcon.before(validators.student.exists)
    def on_get(self, req, resp):
        years = db.Session.query(StudentBatch).filter_by(
            student_id=req.get_json('student_id')
        ).order_by(StudentBatch.batch_year.desc()).all()

        year_ctr = 0
        data = dict()
        data['student'] = dict()
        for year in years:
            data['student'][year_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][year_ctr][scope] = getattr(year, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            year_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student batch years retrieval', 'Batch years successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.student.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        batch_year = req.get_json('batch_year')

        db.Session.add(StudentBatch(student_id, batch_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student batch year successfully', 'New batch year for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    def on_put(self, req, resp):
        student_batch_year = db.Session.query(StudentStatus).filter_by(student_id=req.get_json('student_id'),
                                                                       batch_year=req.get_json('batch_year')
                                                                       ).one()
        student_batch_year.batch_year = req.get_json('batch_year').strip()
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student batch year updated successfully',
            'Batch year of student {0} has been updated.'.format(student_batch_year.student_id)
        )

    @falcon.before(validators.student.exists)
    def on_delete(self, req, resp):
        student_batch_year = db.Session.query(StudentStatus).filter_by(student_id=req.get_json('student_id'),
                                                                       batch_year=req.get_json('batch_year')
                                                                       ).one()
        db.Session.delete(student_batch_year)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student batch year deleted successfully',
            'Batch year of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentMonthlyRequiredDaysController(object):
    @falcon.before(validators.admin.required)
    def on_get(self, req, resp):
        data = dict()
        data['month_days'] = dict()
        if req.get_json('school_year') == '__all__':
            years = StudentMonthlyRequiredDays.query.order_by(StudentMonthlyRequiredDays.school_year.desc()).all()

            row_ctr = 0
            for year in years:
                data['month_days'][row_ctr] = dict()

                for scope in req.scope:
                    try:
                        data['month_days'][row_ctr][scope] = getattr(year, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the rating criteria.')

                row_ctr += 1
        else:
            year = db.Session.query(StudentMonthlyRequiredDays).filter_by(
                school_year=req.get_json('school_year')
            ).one()

            data['month_days'] = dict()
            for scope in req.scope:
                try:
                    data['month_days'][scope] = getattr(year, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the criteria.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful monthly required days retrieval', 'Monthly required days successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    def on_post(self, req, resp):
        month = req.get_json('month')
        school_year = req.get_json('school_year')
        days_required = req.get_json('days_required')

        db.Session.add(StudentMonthlyRequiredDays(month, school_year, days_required))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new monthly required days successfully', 'New required days has been added.'
        )

    @falcon.before(validators.admin.required)
    @falcon.before(validators.student.monthly_attendance_school_year_exists)
    def on_put(self, req, resp):
        student_month_days = db.Session.query(StudentStatus).filter_by(month=req.get_json('month'),
                                                                       school_year=req.get_json('school_year')
                                                                       ).one()
        student_month_days.required_days = req.get_json('required_days').strip()
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Required days for a month updated successfully',
            'Required days of month {0} has been updated.'.format(student_month_days.month)
        )

    @falcon.before(validators.admin.required)
    @falcon.before(validators.student.monthly_attendance_school_year_exists)
    def on_delete(self, req, resp):
        student_month_days = db.Session.query(StudentStatus).filter_by(month_id=req.get_json('month'),
                                                                       school_year=req.get_json('school_year')
                                                                       ).one()
        db.Session.delete(student_month_days)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Month deleted successfully',
            'Month {0} has been deleted.'.format(student_month_days.month)
        )


class StudentMonthlyAttendanceController(object):
    @falcon.before(validators.student.exists)
    def on_get(self, req, resp):
        monthly_attendances = db.Session.query(StudentMonthlyAttendance).filter_by(
            student_id=req.get_json('student_id')
        ).order_by(StudentMonthlyAttendance.school_year.desc(),
                   StudentMonthlyAttendance.quarter.desc(),
                   StudentMonthlyAttendance.month.desc()).all()

        row_ctr = 0
        data = dict()
        data['student'] = dict()
        for monthly_attendance in monthly_attendances:
            data['student'][row_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][row_ctr][scope] = getattr(monthly_attendance, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the student monthly attendance.')

            row_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student attendance retrieval', 'Attendance successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.student.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        month = req.get_json('month')
        quarter = req.get_json('quarter')
        year_level = req.get_json('year_level')
        school_year = req.get_json('school_year')
        days_required = req.get_json('days_required')
        days_present = req.get_json('days_present')
        days_tardy = req.get_json('days_tardy')
        days_absent = req.get_json('days_absent')

        db.Session.add(
            StudentMonthlyAttendance(
                student_id, month, quarter, year_level,
                school_year, days_required, days_present, days_tardy, days_absent
            )
        )
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student attendance successfully', 'New attendance for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    @falcon.before(validators.rating_criteria.exists)
    def on_put(self, req, resp):
        student_attendance = db.Session.query(StudentRating).filter_by(student_id=req.get_json('student_id'),
                                                                       month=req.get_json('month'),
                                                                       quarter=req.get_json('quarter'),
                                                                       year_level=req.get_json('year_level')
                                                                       ).one()

        if 'month' in req.json:
            student_attendance.month = req.get_json('month')

        if 'month' in req.json:
            student_attendance.month = req.get_json('month')

        if 'quarter' in req.json:
            student_attendance.quarter = req.get_json('quarter')

        if 'year_level' in req.json:
            student_attendance.year_level = req.get_json('year_level')

        if 'school_year' in req.json:
            student_attendance.school_year = req.get_json('school_year')

        if 'days_required' in req.json:
            student_attendance.days_required = req.get_json('days_required')

        if 'days_present' in req.json:
            student_attendance.days_present = req.get_json('days_present')

        if 'days_tardy' in req.json:
            student_attendance.days_tardy = req.get_json('days_tardy')

        if 'days_absent' in req.json:
            student_attendance.days_absent = req.get_json('days_absent')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student attendance updated successfully',
            'Attendance of student {0} has been updated.'.format(student_attendance.student_id)
        )

    @falcon.before(validators.student.exists)
    def on_delete(self, req, resp):
        student_attendance = db.Session.query(StudentRating).filter_by(student_id=req.get_json('student_id'),
                                                                       month=req.get_json('month'),
                                                                       quarter=req.get_json('quarter'),
                                                                       year_level=req.get_json('year_level')
                                                                       ).one()
        db.Session.delete(student_attendance)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student attendance deleted successfully',
            'Attendance of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentStatusController(object):
    @falcon.before(validators.student.exists)
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
    @falcon.before(validators.student.exists)
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

    @falcon.before(validators.student.exists)
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
            'Status of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentSubjectController(object):
    @falcon.before(validators.student.exists)
    def on_get(self, req, resp):
        subjects = db.Session.query(StudentSubject).filter_by(
            student_id=req.get_json('student_id')
        ).order_by(StudentSubject.school_year.desc())

        subject_ctr = 0
        data = dict()
        data['student'] = dict()
        for subject in subjects:
            data['student'][subject_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][subject_ctr][scope] = getattr(subject, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            subject_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student statuses retrieval', 'Statuses successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.student.exists)
    @falcon.before(validators.teacher.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        subject_id = req.get_json('subject_id')
        school_year = req.get_json('school_year')
        instructor_id = req.get_json('teacher_id')

        db.Session.add(StudentSubject(student_id, subject_id, school_year, instructor_id))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student subject successfully', 'New subject for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    def on_delete(self, req, resp):
        subject = db.Session.query(StudentSubject).filter_by(student_id=req.get_json('student_id'),
                                                             subject_id=req.get_json('subject_id'),
                                                             school_year=req.get_json('school_year')
                                                             ).one()
        db.Session.delete(subject)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student subject deleted successfully',
            'Subject of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentSubjectGradeController(object):
    @falcon.before(validators.student.exists)
    @falcon.before(validators.subject.exists)
    def on_get(self, req, resp):
        grades = db.Session.query(StudentSubjectGrade).filter_by(
            student_id=req.get_json('student_id'),
            subject_id=req.get_json('subject_id'),
            school_year=req.get_json('school_year')
        ).order_by(StudentSubjectGrade.quarter.desc())

        quarter_ctr = 0
        data = dict()
        data['student'] = dict()
        for grade in grades:
            data['student'][quarter_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][quarter_ctr][scope] = getattr(grade, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            quarter_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student subject grades retrieval', 'Subject grades successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.student.exists)
    @falcon.before(validators.subject.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        subject_id = req.get_json('subject_id')
        school_year = req.get_json('school_year')
        quarter = req.get_json('quarter')
        grade = req.get_json('grade')

        db.Session.add(StudentSubjectGrade(student_id, subject_id, school_year, quarter, grade))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student subject grade successfully', 'New grade for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    @falcon.before(validators.subject.exists)
    def on_put(self, req, resp):
        grade = db.Session.query(StudentSubjectGrade).filter_by(student_id=req.get_json('student_id'),
                                                                subject_id=req.get_json('subject_id'),
                                                                school_year=req.get_json('school_year'),
                                                                quarter=req.get_json('quarter')
                                                                ).one()
        grade.grade = req.get_json('grade').strip()
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student status updated successfully',
            'Status of student {0} has been updated.'.format(grade.student_id)
        )

    @falcon.before(validators.student.exists)
    def on_delete(self, req, resp):
        grade = db.Session.query(StudentSubjectGrade).filter_by(student_id=req.get_json('student_id'),
                                                                subject_id=req.get_json('subject_id'),
                                                                school_year=req.get_json('school_year'),
                                                                quarter=req.get_json('quarter')
                                                                ).one()
        db.Session.delete(grade)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student subject grade deleted successfully',
            'Subject grade of student {0} has been deleted.'.format(req.get_json('student_id'))
        )


class StudentSubjectPendingGradeController(object):
    @falcon.before(validators.student.exists)
    @falcon.before(validators.subject.exists)
    def on_get(self, req, resp):
        grades = db.Session.query(StudentSubjectPendingGrade).filter_by(
            student_id=req.get_json('student_id'),
            subject_id=req.get_json('subject_id'),
            school_year=req.get_json('school_year')
        ).order_by(StudentSubjectPendingGrade.quarter.desc())

        quarter_ctr = 0
        data = dict()
        data['student'] = dict()
        for grade in grades:
            data['student'][quarter_ctr] = dict()

            for scope in req.scope:
                try:
                    data['student'][quarter_ctr][scope] = getattr(grade, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            quarter_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student subject grades retrieval', 'Subject grades successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.student.exists)
    @falcon.before(validators.teacher.exists)
    @falcon.before(validators.subject.exists)
    def on_post(self, req, resp):
        student_id = req.get_json('student_id')
        subject_id = req.get_json('subject_id')
        teacher_id = req.get_json('teacher_id')
        school_year = req.get_json('school_year')
        quarter = req.get_json('quarter')
        grade = req.get_json('grade')

        db.Session.add(StudentSubjectPendingGrade(student_id, subject_id, teacher_id, school_year, quarter, grade))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new student subject grade successfully', 'New grade for {0} has been added.'.format(student_id)
        )

    @falcon.before(validators.student.exists)
    @falcon.before(validators.subject.exists)
    def on_put(self, req, resp):
        grade = db.Session.query(StudentSubjectPendingGrade).filter_by(student_id=req.get_json('student_id'),
                                                                       subject_id=req.get_json('subject_id'),
                                                                       school_year=req.get_json('school_year'),
                                                                       quarter=req.get_json('quarter')
                                                                       ).one()
        grade.grade = req.get_json('grade').strip()
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student status updated successfully',
            'Status of student {0} has been updated.'.format(grade.student_id)
        )

    @falcon.before(validators.student.exists)
    def on_delete(self, req, resp):
        grade = db.Session.query(StudentSubjectPendingGrade).filter_by(student_id=req.get_json('student_id'),
                                                                       subject_id=req.get_json('subject_id'),
                                                                       school_year=req.get_json('school_year'),
                                                                       quarter=req.get_json('quarter')
                                                                       ).one()
        db.Session.delete(grade)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Student subject grade deleted successfully',
            'Subject grade of student {0} has been deleted.'.format(req.get_json('student_id'))
        )
