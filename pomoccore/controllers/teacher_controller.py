# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Teacher
from pomoccore.models import TeacherPosition
from pomoccore.models import TeacherPositionList
from pomoccore.utils import validators
from pomoccore.utils import response


class TeacherController(object):
    @falcon.before(validators.teacher_exists)
    def on_get(self, req, resp):
        data = dict()
        data['teacher'] = dict()
        if req.get_json('id') == '__all__':
            teachers = Teacher.query.all()

            row_ctr = 0
            for teacher in teachers:
                subject_grade_ctr = 0
                pending_subject_grades = dict()
                for subject_grade in teacher.pending_subject_grades:
                    pending_subject_grades[subject_grade_ctr] = {
                        'student_id': subject_grade.student_id,
                        'subject_id': subject_grade.subject_id,
                        'school_year': subject_grade.school_year,
                        'quarter': subject_grade.quarter
                    }

                    subject_grade_ctr += 1

                section_adviser_ctr = 0
                section_advisories = dict()
                for section_advisory in teacher.section_advisories:
                    section_advisories[section_adviser_ctr] = {
                        'section_id': section_advisory.section_id,
                        'school_year': section_advisory.school_year
                    }

                    section_adviser_ctr += 1

                batch_adviser_ctr = 0
                batch_advisories = dict()
                for batch_advisory in teacher.batch_advisories:
                    batch_advisories[batch_adviser_ctr] = {
                        'batch_year': batch_advisory.batch_year,
                        'school_year': batch_advisory.school_year
                    }

                    batch_adviser_ctr += 1

                subject_ctr = 0
                subjects = dict()
                for subject in teacher.subjects:
                    subjects[subject_ctr] = {
                        'subject_id': subject.subject_id,
                        'school_year': subject.school_year,
                        'schedule': subject.schedule
                    }

                    subject_ctr += 1

                data['teachers'][row_ctr] = {
                    'id': teacher.teacher_id,
                    'pending_subject_grades': pending_subject_grades,
                    'section_advisories': section_advisories,
                    'batch_advisories': batch_advisories,
                    'subjects': subjects
                }

                row_ctr += 1
        else:
            teacher = db.Session.query(Teacher).filter_by(teacher_id=req.get_json('id')).one()

            subject_grade_ctr = 0
            pending_subject_grades = dict()
            for subject_grade in teacher.pending_subject_grades:
                pending_subject_grades[subject_grade_ctr] = {
                    'student_id': subject_grade.student_id,
                    'subject_id': subject_grade.subject_id,
                    'school_year': subject_grade.school_year,
                    'quarter': subject_grade.quarter
                }

                subject_grade_ctr += 1

            section_adviser_ctr = 0
            section_advisories = dict()
            for section_advisory in teacher.section_advisories:
                section_advisories[section_adviser_ctr] = {
                    'section_id': section_advisory.section_id,
                    'school_year': section_advisory.school_year
                }

                section_adviser_ctr += 1

            batch_adviser_ctr = 0
            batch_advisories = dict()
            for batch_advisory in teacher.batch_advisories:
                batch_advisories[batch_adviser_ctr] = {
                    'batch_year': batch_advisory.batch_year,
                    'school_year': batch_advisory.school_year
                }

                batch_adviser_ctr += 1

            subject_ctr = 0
            subjects = dict()
            for subject in teacher.subjects:
                subjects[subject_ctr] = {
                    'subject_id': subject.subject_id,
                    'school_year': subject.school_year,
                    'schedule': subject.schedule
                }

                subject_ctr += 1

            data['teacher'] = {
                'id': teacher.teacher_id,
                'pending_subject_grades': pending_subject_grades,
                'section_advisories': section_advisories,
                'batch_advisories': batch_advisories,
                'subjects': subjects
            }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful teacher data retrieval', 'Teacher data successfully gathered.', data
        )


class TeacherPositionController(object):
    @falcon.before(validators.user_exists)
    def on_get(self, req, resp):
        positions = db.Session.query(TeacherPosition).filter_by(
                       teacher_id=req.get_json('id')
                    ).order_by(TeacherPosition.school_year.desc(), TeacherPosition.date_created.desc()).all()

        row_ctr = 0
        data = dict()
        data['teacher'] = dict()
        for position in positions:
            data['teacher'][row_ctr] = {
                'teacher_id': position.teacher_id,
                'position_id': position.position_id,
                'school_year': position.school_year
            }

            row_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful teacher positions retrieval', 'Teacher positions successfully gathered.', data
        )

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.user_exists)
    @falcon.before(validators.teacher_position_exists_2)
    def on_post(self, req, resp):
        teacher_id = req.get_json('id')
        position_id = req.get_json('position_id')
        school_year = req.get_json('school_year')

        db.Session.add(TeacherPosition(teacher_id, position_id, school_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Teacher position created successfully', 'New position {0} has been created.'.format(position_id)
        )

    @falcon.before(validators.user_exists)
    def on_put(self, req, resp):
        position = db.Session.query(TeacherPosition).filter_by(teacher_id=req.get_json('id')).one()

        if 'position_id' in req.json:
            position.position_id = req.get_json('position_id')

        if 'school_year' in req.json:
            position.school_year = req.get_json('school_year')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Teacher position updated successfully', 'Position {0} has been updated.'.format(position.position_id)
        )

    @falcon.before(validators.user_exists)
    @falcon.before(validators.teacher_position_exists_2)
    def on_delete(self, req, resp):
        position = db.Session.query(TeacherPosition).filter_by(teacher_id=req.get_json('id'),
                                                               position_id=req.get_json('position_id'),
                                                               school_year=req.get_json('school_year')).one()

        db.Session.delete(position)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Position deleted successfully', 'Position {0} has been deleted.'.format(position.position_name)
        )


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
