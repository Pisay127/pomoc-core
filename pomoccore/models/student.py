# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import SmallInteger

from .user import UserModel


class Student(UserModel):

    __tablename__ = 'student_account'

    year_level = Column('year_level', SmallInteger, nullable=False)

    def __init__(self, id_number, username, password, first_name,
                 middle_name, last_name, age, birth_date, year_level,
                 profile_picture=None):
        super(Student, self).__init__(id_number, username, password, first_name,
                                      middle_name, last_name, age, birth_date, profile_picture)
        self.year_level = year_level

    def __repr__(self):
        return '<Student {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)
