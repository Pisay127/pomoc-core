# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Teacher(BaseModel):

    __tablename__ = 'teachers'

    id_number = Column('id_number', Text, ForeignKey('users.id_number'),
                       primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref='teachers', uselist=False)

    def __init__(self, id_number):
        self.id_number = id_number

    def __repr__(self):
        return '<Teacher {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)
