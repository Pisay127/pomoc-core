# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon
import json

from pomoccore import db
from pomoccore.models import User


class UserController(object):
    def on_get(self, req, resp):
        # For the time being, we send the id.
        try:
            raw_get_req = (req.stream.read()).decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error!', ex.message)

        try:
            get_req = json.loads(raw_get_req, encoding='utf-8')
            user_id = get_req['id']

            user_info = db.Session.query(User).filter_by(user_id=user_id).first()
            resp.body = json.dumps({'id': user_info.user_id, 'username': user_info.username})
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.')

        resp.status = falcon.HTTP_201

    def on_post(self, req, resp):
        try:
            raw_user_info = (req.stream.read()).decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error!', ex.message)

        try:
            user_info = json.loads(raw_user_info, encoding='utf-8')
            user_id = user_info['id']
            username = user_info['username']
            password = user_info['password']

            user = User(user_id, username, password)
            db.Session.add(user)
            db.Session.commit()
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'message': "success"})
