# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Student
from pomoccore.models.student import StudentStatus
from pomoccore.utils import validators
from pomoccore.utils import response


class StudentController(object):
    @falcon.before(validators.student_exists)
    def on_get(self, req, resp):
        data = dict()
        data['student'] = dict()
        if req.get_json('id') == '__all__':
            students = Student.query.all()

            row_ctr = 0
            for student in students:
                section_ctr = 0
                sections = dict()
                for section in student.sections:
                    sections[section_ctr] = {
                        'section_id': section.section_id,
                        'year_level': section.year_level,
                        'school_year': section.school_year
                    }

                    section_ctr += 1

                rating_ctr = 0
                ratings = dict()
                for rate in student.ratings:
                    ratings[rating_ctr] = {
                        'criterion_id': rate.criterion_id,
                        'rating': rate.rating,
                        'quarter': rate.quarter,
                        'year_level': rate.year_level,
                        'school_year': rate.school_year
                    }

                    rating_ctr += 1

                batch_ctr = 0
                batch = dict()
                for bat in student.batch:
                    batch[batch_ctr] = {
                        'batch_year': bat.batch_year
                    }

                monthly_attendance_ctr = 0
                monthly_attendance = dict()
                for month in student.monthly_attendance:
                    monthly_attendance[monthly_attendance_ctr] = {
                        'month': month.month,
                        'quarter': month.quarter,
                        'year_level': month.year_level,
                        'school_year': month.school_year,
                        'days_present': month.days_present,
                        'days_tardy': month.days_tardy,
                        'days_absent': month.days_absent
                    }

                    monthly_attendance_ctr += 1

                status_ctr = 0
                statuses = dict()
                for stat in student.statuses:
                    statuses[status_ctr] = {
                        'status': stat.status,
                        'quarter': stat.quarter,
                        'year_level': stat.year_level,
                        'school_year': stat.school_year
                    }

                subject_ctr = 0
                subjects = dict()
                for subject in student.subjects:
                    subjects[subject_ctr] = {
                        'subject_id': subject.subject_id,
                        'school_year': subject.school_year,
                        'instructor_id': subject.instructor_id
                    }

                gwa_ctr = 0
                gwa = dict()
                for gwa in student.gwa:
                    gwa[gwa_ctr] = {
                        'gwa': gwa.gwa,
                        'quarter': gwa.quarter,
                        'school_year': gwa.school_year
                    }

                data['student'][row_ctr] = {
                    'id': student.student_id,
                    'year_level': student.year_level,
                    'sections': sections,
                    'ratings': ratings,
                    'batch': batch,
                    'monthly_attendance': monthly_attendance,
                    'statuses': statuses,
                    'subjects': subjects,
                    'gwa': gwa
                }

                row_ctr += 1
        else:
            student = db.Session.query(Student).filter_by(student_id=req.get_json('id')).one()

            section_ctr = 0
            sections = dict()
            for section in student.sections:
                sections[section_ctr] = {
                    'section_id': section.section_id,
                    'year_level': section.year_level,
                    'school_year': section.school_year
                }

                section_ctr += 1

            rating_ctr = 0
            ratings = dict()
            for rate in student.ratings:
                ratings[rating_ctr] = {
                    'criterion_id': rate.criterion_id,
                    'rating': rate.rating,
                    'quarter': rate.quarter,
                    'year_level': rate.year_level,
                    'school_year': rate.school_year
                }

                rating_ctr += 1

            monthly_attendance_ctr = 0
            monthly_attendance = dict()
            for month in student.monthly_attendance:
                monthly_attendance[monthly_attendance_ctr] = {
                    'month': month.month,
                    'quarter': month.quarter,
                    'year_level': month.year_level,
                    'school_year': month.school_year,
                    'days_present': month.days_present,
                    'days_tardy': month.days_tardy,
                    'days_absent': month.days_absent
                }

                monthly_attendance_ctr += 1

            status_ctr = 0
            statuses = dict()
            for stat in student.statuses:
                statuses[status_ctr] = {
                    'status': stat.status,
                    'quarter': stat.quarter,
                    'year_level': stat.year_level,
                    'school_year': stat.school_year
                }

            subject_ctr = 0
            subjects = dict()
            for subject in student.subjects:
                subjects[subject_ctr] = {
                    'subject_id': subject.subject_id,
                    'school_year': subject.school_year,
                    'instructor_id': subject.instructor_id
                }

            gwa_ctr = 0
            gwa = dict()
            for gwa in student.gwa:
                gwa[gwa_ctr] = {
                    'gwa': gwa.gwa,
                    'quarter': gwa.quarter,
                    'school_year': gwa.school_year
                }

            data['student'] = {
                'id': student.student_id,
                'year_level': student.year_level,
                'sections': sections,
                'ratings': ratings,
                'batch': batch,
                'monthly_attendance': monthly_attendance,
                'statuses': statuses,
                'subjects': subjects,
                'gwa': gwa
            }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful student data retrieval', 'Student data successfully gathered.', data
        )


class StudentStatusController(object):
    @falcon.before(validators.user_exists)
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

