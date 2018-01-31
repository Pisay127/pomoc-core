# Copyright (c) 2018 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import VariableSettings
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class VariableSettingsController(object):
    def on_get(self, req, resp):
        setting = db.Session.query(VariableSettings).one()

        data = dict()
        data['setting'] = dict()
        for scope in req.scope:
            try:
                data['setting'][scope] = getattr(setting, scope)
            except AttributeError:
                raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                  'Scope is not part of the user.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful settings retrieval', 'Settings successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    def on_post(self, req, resp):
        current_quarter = req.get_json('current_quarter')
        current_school_year = req.get_json('current_school_year')
        start_month = req.get_json('start_month')
        end_month = req.get_json('end_month')

        db.Session.add(VariableSettings(current_quarter, current_school_year, start_month, end_month))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Settings created successfully', 'Settings has been created.'
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    def on_put(self, req, resp):
        settings = db.Session.query(VariableSettings).one()

        for attrib in req.json:
            if attrib == 'access_token':
                continue

            setattr(settings, attrib, req.get_json(attrib))

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Settings updated successfully', 'Settings has been updated.'
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    def on_delete(self, req, resp):
        settings = db.Session.query(VariableSettings).one()

        db.Session.delete(settings)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Settings deleted successfully', 'Settings has been deleted.'
        )
