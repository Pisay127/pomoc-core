# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy_utils.types import PasswordType

from pomoccore import settings
from .base_model import BaseModel


class User(BaseModel):

    __tablename__ = 'user_accounts'

    user_id = Column('id', Text, primary_key=True, nullable=False)
    username = Column('username', Text, nullable=False)
    password = Column('password', PasswordType(schemes=settings.PASSWORD_SCHEMES), nullable=False)

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Users {0} {1}>'.format(self.user_id, self.username)
