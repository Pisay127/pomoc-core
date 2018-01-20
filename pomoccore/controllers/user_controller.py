# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import User
from pomoccore.models import Admin
from pomoccore.models import Teacher
from pomoccore.models import Student
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class UserController(object):
    @falcon.before(validators.user.exists)
    def on_get(self, req, resp):
        data = dict()
        data['user'] = dict()

        if req.get_json('user_id') == '__all__':
            users = db.Session.query(User).all().order_by(User.last_name.asc(),
                                                          User.first_name.asc(),
                                                          User.middle_name.asc(),
                                                          User.id_number.asc())

            user_ctr = 0
            for user in users:
                data['user'][user_ctr] = dict()

                for scope in req.scope:
                    try:
                        if scope == 'birth_date':
                            data['user'][user_ctr][scope] = user.birth_date.strftime('%Y-%m-%d %H:%M:%S.%f')
                        else:
                            data['user'][user_ctr][scope] = getattr(user, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the user.')
                user_ctr += 1
        else:
            user = db.Session.query(User).filter_by(user_id=req.get_json('user_id')).one()

            data['user'] = dict()
            for scope in req.scope:
                try:
                    if scope == 'birth_date':
                        data['user'][scope] = user.birth_date.strftime('%Y-%m-%d %H:%M:%S.%f')
                    else:
                        data['user'][scope] = getattr(user, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the user.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful user data retrieval', 'User data successfully gathered.', data
        )

    @falcon.before(validators.oauth.access_token_valid)
    @falcon.before(validators.oauth.access_token_user_exists)
    @falcon.before(validators.admin.required)
    @falcon.before(validators.user.not_exists_by_id_number)
    def on_post(self, req, resp):
        id_number = req.get_json('id_number')
        user_type = req.get_json('user_type')
        username = req.get_json('username')
        password = req.get_json('password')
        first_name = req.get_json('first_name')
        middle_name = req.get_json('middle_name')
        last_name = req.get_json('last_name')
        age = req.get_json('age')
        birth_date = req.get_json('birth_date')

        # TODO: Add profile picture upload support.

        new_user = User(id_number, user_type, username, password, first_name,
                        middle_name, last_name, age, birth_date)
        db.Session.add(new_user)
        db.Session.commit()

        if user_type == 'admin':
            db.Session.add(Admin(new_user.user_id))
        elif user_type == 'teacher':
            db.Session.add(Teacher(new_user.user_id))
        else:  # Oh, it's a student then.
            db.Session.add(Student(new_user.user_id, 1))  # Assume that it is a 7th grader.

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_201, 'Ignacio! Where is the damn internal code again?',
            'User created successfully', 'New user {0} has been created.'.format(username)
        )

    @falcon.before(validators.user.exists)
    def on_put(self, req, resp):
        user = db.Session.query(User).filter_by(user_id=req.get_json('user_id')).one()

        # We should not modify the user type. Records will get fucked up.
        # NOTE: Handle profile pictures in the future.

        for attrib in req.json:
            if attrib == 'user_id':
                continue

            if attrib == 'username':  # Dude, we gotta lowercase the string.
                user.username = req.get_json(attrib).strip().lower()
                continue

            setattr(user, attrib, req.get_json(attrib))

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'User updated successfully', 'User {0} has been updated.'.format(user.username)
        )

    @falcon.before(validators.user.exists)
    def on_delete(self, req, resp):
        user = db.Session.query(User).filter_by(user_id=req.get_json('user_id')).one()

        db.Session.delete(user)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'User deleted successfully', 'User {0} has been deleted.'.format(user.username)
        )
