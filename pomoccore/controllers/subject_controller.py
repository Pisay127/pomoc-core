# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Subject
from pomoccore.models import SubjectOffering
from pomoccore.utils import validators
from pomoccore.utils import response


class SubjectController(object):
    @falcon.before(validators.subject_exists)
    def on_get(self, req, resp):
        data = dict()
        data['subject'] = dict()
        if req.get_json('id') == '__all__':
            subjects = Subject.query.all()

            subj_ctr = 0
            for subject in subjects:
                data['subject'][subj_ctr] = {
                    'id': subject.subject_id,
                    'name': subject.subject_name,
                    'year_level': subject.year_level
                }

                subj_ctr += 1
        else:
            retrieved_subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('id')).one()

            data['subject'] = {
                'id': retrieved_subject.subject_id,
                'name': retrieved_subject.subject_name,
                'year_level': retrieved_subject.year_level
            }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful subject data retrieval', 'Subject data successfully gathered.', data
        )

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.subject_not_exists)
    def on_post(self, req, resp):
        name = req.get_json('name')
        year_level = req.get_json('year_level')

        # NOTE: year_level == 1 denotes the seventh grade,
        #       year_level == 2 denotes the eight grade,
        #       and so on.

        db.Session.add(Subject(name, year_level))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Subject created successfully', 'New subject {0} has been created.'.format(name)
        )

    @falcon.before(validators.subject_exists)
    def on_put(self, req, resp):
        retrieved_subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('id')).one()

        if 'name' in req.json:
            retrieved_subject.subject_name = req.get_json('name')

        if 'year_level' in req.json:
            retrieved_subject.year_level = req.get_json('year_level')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Subject updated successfully', 'Subject {0} has been updated.'.format(retrieved_subject.subject_name)
        )

    @falcon.before(validators.subject_exists)
    def on_delete(self, req, resp):
        retrieved_subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('id')).one()

        db.Session.delete(retrieved_subject)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Subject updated successfully', 'Subject {0} has been updated.'.format(retrieved_subject.subject_name)
        )


class SubjectOfferingController(object):
    @falcon.before(validators.subject_exists)
    def on_get(self, req, resp):
        subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('id')).one()

        offering_ctr = 0
        data = dict()
        data['subject_offering'] = dict()
        for offering in subject.offerings:
            data['subject_offering'][offering_ctr] = {
                'subject_id': offering.subject_id,
                'school_year': offering.school_year,
                'instructor_id': offering.instructor_id,
                'schedule': offering.schedule
            }

            offering_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful subject offering retrieval', 'Subject offering successfully gathered.', data
        )

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.subject_offering_not_exists)
    def on_post(self, req, resp):
        subject_id = req.get_json('id')
        school_year = req.get_json('school_year')
        instructor_id = req.get_json('instructor_id')
        schedule = req.get_json('schedule')

        db.Session.add(SubjectOffering(subject_id, school_year, instructor_id, schedule))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Subject offering created successfully', 'New offering {0} has been created.'
        )

    @falcon.before(validators.subject_offering_exists)
    def on_put(self, req, resp):
        offering = db.Session.query(SubjectOffering).filter_by(subject_id=req.get_json('id'),
                                                               school_year=req.get_json('school_year'),
                                                               instructor_id=req.get_json('instructor_id'),
                                                               schedule=req.get_json('schedule')).one()

        if 'school_year' in req.json:
            offering.school_year = req.get_json('school_year')

        if 'instructor_id' in req.json:
            offering.instructor_id = req.get_json('instructor_id')

        if 'schedule' in req.json:
            offering.schedule = req.get_json('schedule')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Offering updated successfully', 'Offering has been updated.'
        )

    @falcon.before(validators.subject_offering_exists)
    def on_delete(self, req, resp):
        offering = db.Session.query(SubjectOffering).filter_by(subject_id=req.get_json('id'),
                                                               school_year=req.get_json('school_year'),
                                                               instructor_id=req.get_json('instructor_id'),
                                                               schedule=req.get_json('schedule')).one()

        db.Session.delete(offering)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Offering deleted successfully', 'Offering has been deleted.'
        )
