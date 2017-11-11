# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import json

import falcon

from pomoccore import db
from pomoccore.models import User
from pomoccore.utils import validators


class UserController(object):
    @falcon.before(validators.user_exists)
    def on_get(self, req, resp):
        retrieved_user = db.Session.query(User).filter_by(username=req.get_json('username')).one()

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({
            'user_id': retrieved_user.user_id,
            'user_type': retrieved_user.user_type,
            'username': retrieved_user.username,
            'first_name': retrieved_user.first_name,
            'middle_name': retrieved_user.middle_name,
            'last_name': retrieved_user.last_name,
            'age': retrieved_user.age,
            'birth_date': retrieved_user.birth_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'profile_picture': retrieved_user.profile_picture
        })

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.new_user_exists)
    def on_post(self, req, resp):
        user_id = req.get_json('user_id')
        user_type = req.get_json('user_type')
        username = req.get_json('username')
        password = req.get_json('password')
        first_name = req.get_json('first_name')
        middle_name = req.get_json('middle_name')
        last_name = req.get_json('last_name')
        age = req.get_json('age')
        birth_date = req.get_json('birth_date')

        profile_picture = None
        if 'profile_picture' in req.json:
            profile_picture = req.get_json('profile_picture')

        db.Session.add(
            User(user_id, user_type, username, password, first_name,
                 middle_name, last_name, age, birth_date, profile_picture)
        )
        db.Session.commit()

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'message': "success"})  # TODO: FIX THIS SHITTY LOOKING SUCCESS RESPONSE.
