# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from .user import UserModel


class Teacher(UserModel):

    __tablename__ = 'teacher_account'

    def __init__(self, id_number, username, password, first_name,
                 middle_name, last_name, age, birth_date, profile_picture=None):
        super(Teacher, self).__init__(id_number, username, password, first_name,
                                      middle_name, last_name, age, birth_date, profile_picture)

    def __repr__(self):
        return '<Teacher {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)
