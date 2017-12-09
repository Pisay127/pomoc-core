# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import jwt

from pomoccore import db

from pomoccore import settings
from pomoccore.models import User
from pomoccore.utils.errors import APIForbiddenError


def required(req, resp, resource, params):
    decoded_token = jwt.decode(
        req.get_json('access_token'), settings.SERVER_SECRET, algorithms='HS256', audience='/', issuer='/'
    )

    user_id = int(decoded_token['sub'])
    retrieved_user = db.Session.query(User).filter_by(user_id=user_id).one()

    if retrieved_user.user_type != 'admin':
        raise APIForbiddenError('Forbidden access', 'User must be an admin.')
