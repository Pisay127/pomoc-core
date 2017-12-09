# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models.grouping import Batch
from pomoccore.utils import validators
from pomoccore.utils import response


class BatchController(object):
    @falcon.before(validators.batch_exists)
    def on_get(self, req, resp):
        data = dict()
        data['batch'] = dict()
        if req.get_json('batch_year') == '__all__':
            batches = Batch.query.all()

            batch_ctr = 0
            for batch in batches:
                data['batch'][batch_ctr] = {
                    'batch_year': batch.batch_year
                }

                batch_ctr += 1

        else:
            retrieved_batch = db.Session.query(Batch).filter_by(batch_year=req.get_json('batch_year')).one()

            data['batch'] = {
                'batch_year': retrieved_batch.batch_year
            }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful batch data retrieval', 'Batch data successfully gathered.', data
        )