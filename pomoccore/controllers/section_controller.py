# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Section
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class SectionController(object):
    @falcon.before(validators.section.exists)
    def on_get(self, req, resp):
        data = dict()
        data['section'] = dict()
        if req.get_json('section_id') == '__all__':
            sections = Section.query.all()

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
    @falcon.before(validators.section.not_exists)
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
            'Section successfully', 'Section {0} has been deleted.'.format(section.section_name)
        )
