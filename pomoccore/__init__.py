# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore.controllers import user_accounts


class API(falcon.API):
    def __init__(self, *args, **kwargs):
        super(API, self).__init__(*args, **kwargs)

        self.add_route('/user', user_accounts.UserController())