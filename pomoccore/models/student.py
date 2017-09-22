# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Student(BaseModel):

    __tablename__ = 'students'

    id_number = Column('id_number', Text, ForeignKey('users.id_number'),
                       primary_key=True, unique=True, nullable=False)
    year_level = Column('year_level', SmallInteger, nullable=False)
    user = relationship('User', backref='students', uselist=False)

    def __init__(self, id_number, year_level):
        self.id_number = id_number
        self.year_level = year_level

    def __repr__(self):
        return '<Student {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)
