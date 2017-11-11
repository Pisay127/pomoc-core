# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from pomoccore import db
from pomoccore import API
from pomoccore.utils import error_serializer
from pomoccore.middleware import db_session_manager

db.init_db()
middleware = [db_session_manager.DBSessionManager(db.Session)]
api = API(middleware=middleware)
api.set_error_serializer(error_serializer.http_json_error_serializer)