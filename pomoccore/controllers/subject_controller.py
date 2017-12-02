# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Subject
from pomoccore.models import SubjectOffering
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class SubjectController(object):
    @falcon.before(validators.subject.exists)
    def on_get(self, req, resp):
        data = dict()
        data['subject'] = dict()
        if req.get_json('subject_id') == '__all__':
            subjects = Subject.query.all().order_by(Subject.subject_name.asc())

            subject_ctr = 0
            for subject in subjects:
                data['subject'][subject_ctr] = dict()

                for scope in req.scope:
                    try:
                        data['subject'][subject_ctr][scope] = getattr(subject, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the user.')

                subject_ctr += 1
        else:
            subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('subject_id')).one()

            data['subject'] = dict()
            for scope in req.scope:
                try:
                    data['subject'][scope] = getattr(subject, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful subject data retrieval', 'Subject data successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.subject.not_exists)
    def on_post(self, req, resp):
        name = req.get_json('subject_name')
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

    @falcon.before(validators.subject.exists)
    def on_put(self, req, resp):
        subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('subject_id')).one()

        if 'subject_name' in req.json:
            subject.subject_name = req.get_json('subject_name')

        if 'year_level' in req.json:
            subject.year_level = req.get_json('year_level')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Subject updated successfully', 'Subject {0} has been updated.'.format(subject.subject_name)
        )

    @falcon.before(validators.subject.exists)
    def on_delete(self, req, resp):
        subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('subject_id')).one()

        db.Session.delete(subject)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Subject updated successfully', 'Subject {0} has been updated.'.format(subject.subject_name)
        )


class SubjectOfferingController(object):
    @falcon.before(validators.subject.exists)
    def on_get(self, req, resp):
        subject = db.Session.query(Subject).filter_by(subject_id=req.get_json('subject_id')).one()

        offering_ctr = 0
        data = dict()
        data['subject_offering'] = dict()
        for offering in subject.offerings:
            data['subject_offering'][offering_ctr] = dict()

            for scope in req.scope:
                try:
                    data['subject_offering'][offering_ctr][scope] = getattr(offering, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

            offering_ctr += 1

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful subject offering retrieval', 'Subject offering successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.subject_offering.not_exists)
    def on_post(self, req, resp):
        subject_id = req.get_json('offering_id')
        school_year = req.get_json('school_year')
        instructor_id = req.get_json('instructor_id')
        schedule = req.get_json('schedule')

        db.Session.add(SubjectOffering(subject_id, school_year, instructor_id, schedule))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Subject offering created successfully', 'New offering {0} has been created.'
        )

    @falcon.before(validators.subject_offering.exists)
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

    @falcon.before(validators.subject_offering.exists)
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
