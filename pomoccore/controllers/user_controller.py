# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import json

import falcon
import jwt

from jwt import ExpiredSignatureError
from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore import settings
from pomoccore.models import User


class UserController(object):
    def on_get(self, req, resp):
        try:
            user_info_request = (req.stream.read()).decode('utf-8')
        except Exception as ex:
            resp.status = falcon.HTTP_400
            resp.body = UserController._get_error_response(
                falcon.HTTP_400, 'Something went wrong', str(ex)
            )
            return

        try:
            request_json = json.loads(user_info_request, encoding='utf-8')
            username = request_json['username']

            try:
                retrieved_user = db.Session.query(User).filter_by(username=username).one()
            except NoResultFound:
                resp.status = falcon.HTTP_404
                resp.body = UserController._get_error_response(
                                            falcon.HTTP_404,
                                            'User could not be found',
                                            'User does not exist or used to be.'
                                            )
                return

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
        except ValueError:
            resp.status = falcon.HTTP_400
            resp.body = UserController._get_error_response(
                falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.'
            )
            return

    def on_post(self, req, resp):
        try:
            user_info_request = (req.stream.read()).decode('utf-8')
        except Exception as ex:
            resp.status = falcon.HTTP_400
            resp.body = UserController._get_error_response(
                falcon.HTTP_400, 'Something went wrong', str(ex)
            )
            return

        try:
            request_json = json.loads(user_info_request, encoding='utf-8')
            user_id = request_json['user_id']
            user_type = request_json['user_type']
            username = request_json['username']
            password = request_json['password']
            first_name = request_json['first_name']
            middle_name = request_json['middle_name']
            last_name = request_json['last_name']
            age = request_json['age']
            birth_date = request_json['birth_date']

            profile_picture = None
            if 'profile_picture' in request_json:
                profile_picture = request_json['profile_picture']

            if 'access_token' in request_json:
                try:
                    decoded_token = jwt.decode(
                        request_json['access_token'],
                        settings.SERVER_SECRET,
                        algorithms='HS256',
                        audience='/',
                        issuer='/'
                    )

                    # Check if user is allowed to create new users.
                    requesting_user = decoded_token['sub']

                    try:
                        retrieved_user = db.Session.query(User).filter_by(username=username).one()
                    except NoResultFound:
                        # Who knows? The access token could still be valid but the user no longer
                        # exists.
                        resp.status = falcon.HTTP_404
                        resp.body = UserController._get_error_response(
                            falcon.HTTP_404,
                            'User could not be found',
                            'User does not exist or used to be.'
                        )
                        return

                    if retrieved_user.user_type != 'admin':
                        resp.status = falcon.HTTP_403
                        resp.body = json.dumps(
                            UserController._get_error_response(
                                403, 'Forbidden', 'Request is forbidden.'
                            )
                        )
                        return

                    new_user = User(user_id, user_type, username, password, first_name, middle_name, last_name,
                                    age, birth_date, profile_picture)
                    db.Session.add(new_user)
                    db.Session.commit()

                    resp.status = falcon.HTTP_201
                    resp.body = json.dumps({'message': "success"})
                except ExpiredSignatureError as ex:
                    resp.status = falcon.HTTP_400
                    resp.body = UserController._get_error_response(
                        falcon.HTTP_400, 'Access token error', 'Invalid or expired access token.'
                    )
                    return
            else:
                resp.status = falcon.HTTP_403
                resp.body = json.dumps(
                    UserController._get_error_response(403, 'Forbidden', 'Request is forbidden.')
                )
        except ValueError:
            resp.status = falcon.HTTP_400
            resp.body = UserController._get_error_response(
                falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.'
            )
            return

    @staticmethod
    def _get_error_response(error_code, error_type, error_message):
        return {
            'status':
            {
                'error': True,
                'code': error_code,
                'type': error_type,
                'message': error_message
            }
        }
