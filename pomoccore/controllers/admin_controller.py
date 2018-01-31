# Copyright (c) 2018 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore import db
from pomoccore.models import User
from pomoccore.models import Admin
from pomoccore.utils import validators
from pomoccore.utils import response
from pomoccore.utils.errors import APIUnprocessableEntityError


class AdminByUsernameController(object):
    @falcon.before(validators.admin.username_exists)
    def on_get(self, req, resp):
        admin = db.Session.query(User).filter_by(username=req.get_json('username')).one()

        data = dict()
        data['admin'] = dict()
        for scope in req.scope:
            try:
                data['admin'][scope] = getattr(admin, scope)
            except AttributeError:
                raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                  'Scope is not part of the teacher.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful admin data retrieval', 'Admin data successfully gathered.', data
        )


class AdminController(object):
    @falcon.before(validators.admin.exists)
    def on_get(self, req, resp):
        data = dict()
        data['admin'] = dict()
        if req.get_json('admin_id') == '__all__':
            admins = db.Session.query(User).filter_by(user_type='admin').order_by(User.last_name.asc(),
                                                                                  User.first_name.asc(),
                                                                                  User.middle_name.asc(),
                                                                                  User.id_number.asc()).all()

            row_ctr = 0
            for admin in admins:
                data['admin'][row_ctr] = dict()
                for scope in req.scope:
                    try:
                        if scope == 'birth_date':
                            data['admin'][row_ctr][scope] = getattr(admin, scope).strftime('%B %d, %Y')
                        else:
                            data['admin'][row_ctr][scope] = getattr(admin, scope)
                    except AttributeError:
                        raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                          'Scope is not part of the admin.')

                row_ctr += 1
        else:
            admin = db.Session.query(Admin).filter_by(admin_id=req.get_json('admin_id')).one()

            data['admin'] = dict()
            for scope in req.scope:
                try:
                    data['admin'][scope] = getattr(admin, scope)
                except AttributeError:
                    raise APIUnprocessableEntityError('Invalid scope \'{0}\''.format(scope),
                                                      'Scope is not part of the admin.')

        response.set_successful_response(
            resp, falcon.HTTP_200, 'Ignacio! Where is the damn internal code?',
            'Successful admin data retrieval', 'Admin data successfully gathered.', data
        )
