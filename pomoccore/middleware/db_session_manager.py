# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.


class DBSessionManager:
    def __init__(self, session):
        self.Session = session

    def process_resource(self, request, response, resource, params):
        resource.session = self.Session()

    def process_response(self, request, response, resource, request_succeeded):
        if hasattr(resource, 'session'):
            if not request_succeeded:
                resource.session.rollback()
            resource.session.close()
