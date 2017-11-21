# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import json
import time
import string
import random

import falcon
import jwt

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound

from pomoccore import db
from pomoccore import settings
from pomoccore.models import User
from pomoccore.models import FirstPartyApp
from pomoccore.models import ClientApp
from pomoccore.utils.errors import APIUnauthorizedError


class OAuthController(object):
    def on_post(self, req, resp):
        grant_type = req.get_json('grant_type')
        client_id = req.get_json('client_id')
        client_secret = req.get_json('client_secret')

        try:
            queried_client = db.Session.query(ClientApp).filter(ClientApp.app_id == client_id).one()
            client_authenticated = (queried_client.app_secret == client_secret)
        except NoResultFound:
            raise APIUnauthorizedError('Unauthorized', 'Client ID does not exist or the secret is incorrect')

        if client_authenticated:
            if grant_type == 'password':
                username = req.get_json('username')
                password = req.get_json('password')
                resp = OAuthController._perform_password_grant(resp, client_id, username, password)
            elif grant_type == 'client_credentials':
                # No scope for now.
                resp = OAuthController._perform_client_credentials_grant(resp, client_id)

    #@staticmethod
    #def _perform_refresh_token_grant():

    @staticmethod
    def _perform_client_credentials_grant(resp, client_id):
        client_is_first_party = db.Session.query(
            exists().where(FirstPartyApp.app_id == client_id)
        ).scalar()  # Only allow Client Credentials Grant for first-party apps for now.

        if client_is_first_party:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({
                'token_type': "bearer",
                'access_token': OAuthController._generate_access_token(client_id).decode('utf-8')
            })
        else:
            resp.status = falcon.HTTP_403
            resp.body = json.dumps(
                OAuthController._get_error_response(403, 'Forbidden', 'Client must be a first party app.')
            )

        return resp

    @staticmethod
    def _perform_password_grant(resp, client_id, username, password):
        client_is_first_party = db.Session.query(
            exists().where(FirstPartyApp.app_id == client_id)
        ).scalar()

        if client_is_first_party:
            try:
                current_user = db.Session.query(User).filter_by(username=username).one()
                if current_user.password == password:
                    access_token = OAuthController._generate_access_token(current_user.user_id).decode('utf-8')
                    refresh_token = OAuthController._generate_refresh_token(settings.TOKEN_SECRET_LENGTH)

                    # Store refresh token to DB

                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps({
                        'token_type': "bearer",
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    })

                    return resp
            except NoResultFound:
                resp.status = falcon.HTTP_401
                resp.body = json.dumps(
                    OAuthController._get_error_response(
                        401,
                        'Unauthorized',
                        'Authentication failure. Incorrect username/password combination.'
                    )
                )

                return resp

            resp.status = falcon.HTTP_401
            resp.body = json.dumps(
                OAuthController._get_error_response(
                    401,
                    'Unauthorized',
                    'Authentication failure. Incorrect username/password combination.'
                )
            )
        else:
            resp.status = falcon.HTTP_403
            resp.body = json.dumps(
                OAuthController._g▼
Logoutet_error_response(403, 'Forbidden', 'Client must be a first party app.')
            )

        return resp

    @staticmethod
    def _generate_access_token(subject):
        return jwt.encode(
            {
                'iss': "/",  # Whole site
                'aud': "/",  # Whole site (again)
                'sub': subject,
                'iat': time.time(),
                'exp': time.time() + settings.ACCESS_TOKEN_EXPIRES
            },
            settings.SERVER_SECRET,
            algorithm='HS256'
        )

    @staticmethod
    def _generate_refresh_token(token_length):
        token = ''
        symbol_set = string.ascii_letters + string.digits + '!@#$%^&*()_+-='

        for _ in range(0, token_length):
            token += random.choice(symbol_set)

        return token

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
