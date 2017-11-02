# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore.controllers import client_app_controller
from pomoccore.controllers import oauth_controller


class API(falcon.API):
    def __init__(self, *args, **kwargs):
        super(API, self).__init__(*args, **kwargs)

        self.add_route('/client_app', client_app_controller.ClientAppController())
        self.add_route('/oauth', oauth_controller.OAuthController())