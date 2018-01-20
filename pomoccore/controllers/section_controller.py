# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Section
from pomoccore.models import SectionAdvisor
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class SectionController(object):
    @falcon.before(validators.section.exists)
    def on_get(self, req, resp):
        data = dict()
        data['section'] = dict()
        if req.get_json('section_id') == '__all__':
            sections = db.Session.query(Section).order_by(Section.year_level.asc(),
                                                          Section.section_name.asc())

            section_ctr = 0
            for section in sections:
                data['section'][section_ctr] = dict()

                for scope in req.scope:
                    try:
                        data['section'][section_ctr][scope] = getattr(section, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the user.')

                section_ctr += 1
        else:
            section = db.Session.query(Section).filter_by(section_id=req.get_json('section_id')).one()

            data['section'] = dict()
            for scope in req.scope:
                try:
                    data['section'][scope] = getattr(section, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful section data retrieval', 'Section data successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.section.name_not_exists)
    def on_post(self, req, resp):
        name = req.get_json('section_name')
        year_level = req.get_json('year_level')

        # NOTE: year_level == 1 denotes the seventh grade,
        #       year_level == 2 denotes the eight grade,
        #       and so on.

        db.Session.add(Section(name, year_level))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Section created successfully', 'New section {0} has been created.'.format(name)
        )

    @falcon.before(validators.section.exists)
    def on_put(self, req, resp):
        section = db.Session.query(Section).filter_by(section_id=req.get_json('section_id')).one()

        if 'name' in req.json:
            section.section_name = req.get_json('section_name')

        if 'year_level' in req.json:
            section.year_level = req.get_json('year_level')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Section updated successfully', 'Section {0} has been updated.'.format(section.section_name)
        )

    @falcon.before(validators.section.exists)
    def on_delete(self, req, resp):
        section = db.Session.query(Section).filter_by(section_id=req.get_json('section_id')).one()

        db.Session.delete(section)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Section successfully', 'Section {0} has been deleted.'.format(req.get_json('section_id'))
        )


class SectionAdvisorByYearController(object):
    @falcon.before(validators.batch.exists)
    def on_get(self, req, resp):
        section_advisors = db.Session.query(SectionAdvisor).filter_by(
            section_id=req.get_json('section_id')
        ).all().order_by(SectionAdvisor.section_id.desc(),
                         SectionAdvisor.school_year.desc())

        data = dict()
        data['section'] = dict()

        ctr = 0
        for section_advisor in section_advisors:
            data['section'][ctr] = dict()
            for scope in req.scope:
                try:
                    data['section'][ctr][scope] = getattr(section_advisor, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the student.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful section advisor data retrieval', 'Section advisor data successfully gathered.', data
        )


class SectionAdvisorController(object):  # This controller gets the advisor by section advisor.
    @falcon.before(validators.teacher.exists)
    def on_get(self, req, resp):
        data = dict()
        section_advisors = db.Session.query(SectionAdvisor).filter_by(
            advisor=req.get_json('teacher_id')
        ).all().order_by(SectionAdvisor.batch_year.desc(),
                         SectionAdvisor.school_year.desc())

        data = dict()
        data['batch'] = dict()

        ctr = 0
        for section_advisor in section_advisors:
            data['section'][ctr] = dict()
            for scope in req.scope:
                try:
                    data['section'][ctr][scope] = getattr(section_advisor, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the student.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful section advisor data retrieval', 'Section advisor data successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.section.exists)
    @falcon.before(validators.teacher.exists)
    @falcon.before(validators.admin.required)
    def on_post(self, req, resp):
        section_id = req.get_json('section_id')
        school_year = req.get_json('school_year')
        advisor_id = req.get_json('teacher_id')

        db.Session.add(SectionAdvisor(section_id, school_year, advisor_id))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new section advisor successfully', 'New section advisor has been added.'
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.teacher.exists)
    @falcon.before(validators.teacher.new_exists)
    @falcon.before(validators.batch.exists)
    def on_put(self, req, resp):
        section_advisor = db.Session.query(SectionAdvisor).filter_by(section_id=req.get_json('section_id'),
                                                                     school_year=req.get_json('school_year'),
                                                                     advisor=req.get_json('teacher_id')).one()

        if 'teacher_id' in req.json:
            section_advisor.advisor = req.get_json('new_teacher_id')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Section advisor updated successfully',
            'Section advisor has been updated.'
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.teacher.exists)
    @falcon.before(validators.section.exists)
    def on_delete(self, req, resp):
        section_advisor = db.Session.query(SectionAdvisor).filter_by(section_id=req.get_json('section_id'),
                                                                     school_year=req.get_json('school_year'),
                                                                     advisor=req.get_json('teacher_id')).one()

        db.Session.delete(section_advisor)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Section advisor deleted successfully',
            'Section advisor has been deleted.'
        )
