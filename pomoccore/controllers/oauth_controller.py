# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import json
import time
import string
import random

import falcon
import jwt

from sqlalchemy import exists
from sqlalchemy import and_

from pomoccore import db
from pomoccore import settings
from pomoccore.models import User
from pomoccore.models import FirstPartyApp
from pomoccore.models import ClientApp


class OAuthController(object):
    def on_post(self, req, resp):
        try:
            oauth_request = (req.stream.read()).decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Something went wrong', ex.message)

        try:
            request_json = json.loads(oauth_request, encoding='utf-8')
            grant_type = request_json['grant_type']
            username = request_json['username']
            password = request_json['password']
            client_id = request_json['client_id']
            client_secret = request_json['client_secret']

            # We did it this way so that we would be able to easily support future OAuth 2.0 flows.
            client_authenticated = db.Session.query(
                exists().where(and_(
                    ClientApp.app_id == client_id, ClientApp.app_secret == client_secret
                ))
            ).scalar()

            if client_authenticated:
                client_is_first_party = db.Session.query(
                    exists().where(FirstPartyApp.app_id == client_id)
                ).scalar()

                if client_is_first_party and grant_type == 'password':
                    current_user = db.Session.query(User).filter_by(username=username, password=password).one()
                    if current_user is None:
                        resp.status = falcon.HTTP_401
                        resp.body = json.dumps(
                            OAuthController._get_error_response(
                                401,
                                'Unauthorized',
                                'Authentication failure. Incorrect username/password combination.'
                            )
                        )
                    else:
                        resp.status = falcon.HTTP_200
                        resp.body = json.dumps({
                            'token_type': "bearer",
                            'access_token': OAuthController._generate_access_token(username),
                            'refresh_token': OAuthController._generate_refresh_token(32)
                        })
                else:
                    resp.status = falcon.HTTP_403
                    resp.body = json.dumps(
                        OAuthController._get_error_response(403, 'Forbidden', 'Client must be a first party app.')
                    )
            else:
                resp.status = falcon.HTTP_401
                resp.body = json.dumps(
                    OAuthController._get_error_response(401, 'Unauthorized', 'Client ID does not exist.')
                )
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.')

    @staticmethod
    def _generate_access_token(username):
        return jwt.encode(
            {
                'iss': "/",  # Whole site
                'aud': "/",  # Whole site (again)
                'sub': username,
                'iat': time.time(),
                'exp': time.time() + settings.TOKEN_EXPIRES,
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
