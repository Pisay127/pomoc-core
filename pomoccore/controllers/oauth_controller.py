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
            client_id = request_json['client_id']
            client_secret = request_json['client_secret']

            # We did it this way so that we would be able to easily support future OAuth 2.0 flows.
            client_authenticated = db.Session.query(
                exists().where(and_(
                    ClientApp.app_id == client_id, ClientApp.app_secret == client_secret
                ))
            ).scalar()

            if client_authenticated:
                if grant_type == 'password':
                    username = request_json['username']
                    password = request_json['password']
                    resp = OAuthController._perform_password_grant(resp, client_id, username, password)
                elif grant_type == 'client_credentials':
                    # No scope for now.
                    resp = OAuthController._perform_client_credentials_grant(resp, client_id)
            else:
                resp.status = falcon.HTTP_401
                resp.body = json.dumps(
                    OAuthController._get_error_response(401, 'Unauthorized', 'Client ID does not exist.')
                )
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.')

    @staticmethod
    def _perform_client_credentials_grant(resp, client_id):
        client_is_first_party = db.Session.query(
            exists().where(FirstPartyApp.app_id == client_id)
        ).scalar()  # Only allow Client Credentials Grant for first-party apps for now.

        if client_is_first_party:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({
                'token_type': "bearer",
                'access_token': OAuthController._generate_access_token(client_id)
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
                access_token = OAuthController._generate_access_token(username)
                refresh_token = OAuthController._generate_refresh_token(settings.TOKEN_SECRET_LENGTH)

                # Store refresh token to DB

                resp.status = falcon.HTTP_200
                resp.body = json.dumps({
                    'token_type': "bearer",
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })
        else:
            resp.status = falcon.HTTP_403
            resp.body = json.dumps(
                OAuthController._get_error_response(403, 'Forbidden', 'Client must be a first party app.')
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
