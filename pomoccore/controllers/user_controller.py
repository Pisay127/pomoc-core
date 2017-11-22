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


class UserController(object):
    @falcon.before(validators.user_exists)
    def on_get(self, req, resp):
        retrieved_user = db.Session.query(User).filter_by(user_id=req.get_json('id')).one()

        data = {
            'user': {
                'id': retrieved_user.id_number,
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
    @falcon.before(validators.user_not_exists)
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

    @falcon.before(validators.user_exists)
    def on_put(self, req, resp):
        retrieved_user = db.Session.query(User).filter_by(user_id=req.get_json('id')).one()

        if 'id_number' in req.json:
            retrieved_user.id_number = req.get_json('id_number')

        # We should not modify the user type. Records will get fucked up.

        if 'username' in req.json:
            retrieved_user.username = req.get_json('username').strip().lower()

        if 'password' in req.json:
            retrieved_user.password = req.get_json('password')

        if 'first_name' in req.json:
            retrieved_user.password = req.get_json('first_name').strip()

        if 'middle_name' in req.json:
            retrieved_user.middle_name = req.get_json('middle_name').strip()

        if 'last_name' in req.json:
            retrieved_user.last_name = req.get_json('last_name').strip()

        if 'age' in req.json:
            retrieved_user.age = req.get_json('age')

        if 'birth_date' in req.json:
            retrieved_user.birth_date = req.get_json('birth_date')

        # NOTE: Handle profile pictures in the future.

        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'User updated successfully', 'User {0} has been updated.'.format(retrieved_user.username)
        )

    @falcon.before(validators.user_exists)
    def on_delete(self, req, resp):
        retrieved_user = db.Session.query(User).filter_by(user_id=req.get_json('id')).one()

        db.Session.delete(retrieved_user)
        db.Session.commit()

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code again?',
            'User deleted successfully', 'User {0} has been deleted.'.format(retrieved_user.subject_name)
        )
