# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy.schema import ForeignKey
from .base_model import BaseModel


class Admin(BaseModel):

    __tablename__ = 'admin_account'

    admin_id = Column('id', BigInteger,
                      ForeignKey('user.id', onupdate='cascade', ondelete='cascade'),
                      primary_key=True, nullable=False, unique=True)

    def __init__(self, admin_id):
        self.admin_id = admin_id

    def __repr__(self):
        return '<Admin {0}'.format(self.admin_id)
