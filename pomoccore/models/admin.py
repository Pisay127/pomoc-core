# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import Integer
from sqlalchemy import Boolean

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


class Section(BaseModel):

    __tablename__ = 'section'

    section_name = Column('section_name', Text, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)
    active = Column('active', Boolean, nullable=False, default=True)

    def __init__(self, section_name, year_level, active=True):
        self.section_name = section_name
        self.year_level = year_level
        self.active = active

    def __repr__(self):
        return '<Section {0}'.format(self.section_name)


class StudentCharacterRatingCriteria(BaseModel):

    __tablename__ = 'student_character_rating_criteria'

    criterion_id = Column('criterion_id', SmallInteger, primary_key=True, nullable=False)
    criterion_description = Column('criterion_description', Text, primary_key=True, nullable=False)

    def __init__(self, criterion_id, criterion_description):
        self.criterion_id = criterion_id
        self.criterion_description = criterion_description

    def __repr__(self):
        return '<StudentCharacterRatingCriteria {0}'.format(self.criterion_id)


class Batch(BaseModel):

    __tablename__ = 'batch'

    batch_year = Column('batch', Integer, primary_key=True, nullable=False)

    def __init__(self, batch_year):
        self.batch_year = batch_year

    def __repr__(self):
        return '<Batch {0}>'.format(self.batch_year)
