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
            raise falcon.HTTPError(falcon.HTTP_400, 'Something went wrong', ex.message)

        try:
            app_info = json.loads(raw_user_info, encoding='utf-8')
            app_id = app_info['app_id']

            app_secret = ClientAppController._generate_app_secret(settings.TOKEN_SECRET_LENGTH)

            client_app = ClientApp(app_id, app_secret)
            first_party_app = FirstPartyApp(app_id)  # We should set it to first party for now.
            db.Session.add(client_app)
            db.Session.add(first_party_app)
            db.Session.commit()
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON', 'Could not decode the request body.')

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'message': "success", 'client_secret': app_secret})

    @staticmethod
    def _generate_app_secret(secret_length):
        secret = ''
        symbol_set = string.ascii_letters + string.digits + '!@#$%^&*()_+-='

        for _ in range(0, secret_length):
            secret += random.choice(symbol_set)

        return secret