# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from pomoccore import db
from pomoccore import API
from pomoccore.utils import error_serializer
from pomoccore.middleware import db_session_manager
from pomoccore.middleware import jsonify
from pomoccore.middleware import scope_retrieval

db.init_db()

api = API(middleware=[
    db_session_manager.DBSessionManager(db.Session),
    jsonify.APIJsonify(),
    scope_retrieval.ScopeRetrieval()
])

api.set_error_serializer(error_serializer.http_json_error_serializer)