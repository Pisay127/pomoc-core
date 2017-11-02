# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon
import json
import string
import random

from pomoccore import db
from pomoccore import settings
from pomoccore.models import ClientApp
from pomoccore.models import FirstPartyApp


class ClientAppController(object):
    # Temporary
    def on_post(self, req, resp):
        try:
            raw_app_info = (req.stream.read()).decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Something went wrong', str(ex))

        try:
            app_id = ClientAppController._generate_app_token(settings.TOKEN_SECRET_LENGTH)
            app_secret = ClientAppController._generate_app_token(settings.TOKEN_SECRET_LENGTH)

            client_app = ClientApp(app_id, app_secret)
            first_party_app = FirstPartyApp(app_id)  # We should make it a first party for now.
            db.Session.add(client_app)
            db.Session.add(first_party_app)
            db.Session.commit()
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'message': "success", 'client_id': app_id, 'client_secret': app_secret})

    @staticmethod
    def _generate_app_token(secret_length):
        token = ''
        symbol_set = string.ascii_letters + string.digits + '!@#$%^&*()_+-='

        for _ in range(0, secret_length):
            token += random.choice(symbol_set)

        return token