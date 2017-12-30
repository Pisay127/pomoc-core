# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models.grouping import Batch
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class BatchController(object):
    @falcon.before(validators.batch.exists)
    def on_get(self, req, resp):
        data = dict()
        data['batch'] = dict()
        if req.get_json('batch_year') == '__all__':
            batches = Batch.query.all()

            batch_ctr = 0
            for batch in batches:
                data['batch'][batch_ctr] = dict()

                for scope in req.scope:
                    try:
                        data['batch'][batch_ctr][scope] = getattr(batch, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the student.')

                batch_ctr += 1

        else:
            retrieved_batch = db.Session.query(Batch).filter_by(batch_year=req.get_json('batch_year')).one()

            data['batch'] = dict()

            for scope in req.scope:
                try:
                    data['student'][scope] = getattr(retrieved_batch, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the student.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful batch data retrieval', 'Batch data successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.batch.not_exists)
    @falcon.before(validators.admin.required)
    def on_get(self, req, resp):
        batch_year = req.get_json('batch_year')

        db.Session.add(Batch(batch_year))
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'Added new batch year successfully', 'New batch year {0} has been added.'.format(batch_year)
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.batch.exists)
    def on_put(self, req, resp):
        batch = db.Session.query(Batch).filter_by(batch_year=req.get_json('batch_year')).one()

        if 'batch_year' in req.json:
            batch.batch_year = req.get_json('batch_year')

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Batch year updated successfully',
            'Batch year has been updated.'
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.batch.exists)
    def on_put(self, req, resp):
        batch = db.Session.query(Batch).filter_by(batch_year=req.get_json('batch_year')).one()

        db.Session.delete(batch)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'Batch year deleted successfully',
            'Batch year has been deleted.'
        )
