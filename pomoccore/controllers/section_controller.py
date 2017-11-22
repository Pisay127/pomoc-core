# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import Section
from pomoccore.utils import validators
from pomoccore.utils import response


class SectionController(object):
    @falcon.before(validators.section_exists)
    def on_get(self, req, resp):
        data = dict()
        data['section'] = dict()
        if req.get_json('id') == '__all__':
            sections = Section.query.all()

            section_ctr = 0
            for section in sections:
                data['section'][section_ctr] = {
                    'id': section.section_id,
                    'name': section.section_name,
                    'year_level': section.year_level
                }

                section_ctr += 1
        else:
            retrieved_section = db.Session.query(Section).filter_by(section_id=req.get_json('id')).one()

            data['section'] = {
                'id': retrieved_section.subject_id,
                'name': retrieved_section.subject_name,
                'year_level': retrieved_section.year_level
            }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful section data retrieval', 'Section data successfully gathered.', data
        )

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.section_not_exists)
    def on_post(self, req, resp):
        name = req.get_json('name')
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

    @falcon.before(validators.section_exists)
    def on_put(self, req, resp):
        retrieved_section = db.Session.query(Section).filter_by(section_id=req.get_json('id')).one()

        if 'name' in req.json:
            retrieved_section.section_name = req.get_json('name')

        if 'year_level' in req.json:
            retrieved_section.year_level = req.get_json('year_level')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Section updated successfully', 'Section {0} has been updated.'.format(retrieved_section.section_name)
        )

    @falcon.before(validators.section_exists)
    def on_delete(self, req, resp):
        retrieved_section = db.Session.query(Section).filter_by(section_id=req.get_json('id')).one()

        db.Session.delete(retrieved_section)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Subject updated successfully', 'Subject {0} has been updated.'.format(retrieved_section.section_name)
        )
