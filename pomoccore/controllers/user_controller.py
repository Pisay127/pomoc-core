# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import User
from pomoccore.utils import validators
from pomoccore.utils import response


class UserController(object):
    @falcon.before(validators.user_exists)
    def on_get(self, req, resp):
        retrieved_user = db.Session.query(User).filter_by(user_id=req.get_json('user_id')).one()

        data = {
            'user': {
                'user_id': retrieved_user.user_id,
                'user_type': retrieved_user.user_type,
                'username': retrieved_user.username,
                'first_name': retrieved_user.first_name,
                'middle_name': retrieved_user.middle_name,
                'last_name': retrieved_user.last_name,
                'age': retrieved_user.age,
                'birth_date': retrieved_user.birth_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                'profile_picture': retrieved_user.profile_picture
            }
        }

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful user data retrieval', 'User data successfully gathered.', data
        )

    @falcon.before(validators.validate_access_token)
    @falcon.before(validators.access_token_requesting_user_exists)
    @falcon.before(validators.admin_required)
    @falcon.before(validators.user_already_exists)
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

        # TODO: Add profile picture upload support.

        db.Session.add(
            User(user_id, user_type, username, password, first_name,
                 middle_name, last_name, age, birth_date)
        )
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'User created successfully', 'New user {0} has been created.'.format(username)
        )
