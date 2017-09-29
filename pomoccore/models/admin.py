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


class StudentCharacterRatingCriteria(BaseModel):

    __tablename__ = 'student_character_rating_criteria'

    criterion_id = Column('criterion_id', SmallInteger, primary_key=True, nullable=False)
    criterion_description = Column('criterion_description', Text, primary_key=True, nullable=False)

    def __init__(self, criterion_id, criterion_description):
        self.criterion_id = criterion_id
        self.criterion_description = criterion_description

    def __repr__(self):
        return '<StudentCharacterRatingCriteria {0}'.format(self.criterion_id)
