# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import SmallInteger

from .base_model import BaseModel
from .user import UserModel


class Admin(UserModel):

    __tablename__ = 'admin_account'

    def __init__(self, id_number, username, password, first_name,
                 middle_name, last_name, age, birth_date, profile_picture=None):
        super(Admin, self).__init__(id_number, username, password, first_name,
                                    middle_name, last_name, age, birth_date, profile_picture)

    def __repr__(self):
        return '<Admin {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)
