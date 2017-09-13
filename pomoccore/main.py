# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.controllers import user_accounts
from pomoccore.middleware import db_session_manager

api = falcon.API(middleware=[db_session_manager.DBSessionManager(db.Session)])
api.add_route('/quote', user_accounts.UsersController())