# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy_utils.types import PasswordType

from pomoccore import settings

from .base_model import Base


class User(Base):

    __tablename__ = 'user'

    user_id = Column('id', BigInteger, primary_key=True, nullable=False, autoincrement=True, unique=True)
    id_number = Column('user_id', Text, nullable=False, unique=True)
    user_type = Column('user_type', Text, nullable=False)
    username = Column('username', Text, nullable=False, unique=True)
    password = Column('password', PasswordType(schemes=settings.PASSWORD_SCHEMES), nullable=False)
    first_name = Column('first_name', Text, nullable=False)
    middle_name = Column('middle_name', Text, nullable=False)
    last_name = Column('last_name', Text, nullable=False)
    age = Column('age', SmallInteger, nullable=False)
    birth_date = Column('birth_date', DateTime, nullable=False)
    profile_picture = Column('profile_picture', Text, nullable=False, default='{directory to default image}')

    def __init__(self, id_number, user_type, username, password, first_name,
                 middle_name, last_name, age, birth_date, profile_picture=None):

        self.id_number = id_number.strip()
        self.user_type = user_type.strip().lower()
        self.username = username.strip().lower()
        self.password = password.strip()
        self.first_name = first_name.strip()
        self.middle_name = middle_name.strip()
        self.last_name = last_name.strip()
        self.age = age.strip()
        self.birth_date = birth_date  # Note to convert `birth_date` to something matches its type (DateTime)

        if profile_picture:
            self.profile_picture = profile_picture

    def __repr__(self):
        return '<User {0}>'.format(self.id_number)


class UserAccessTokens(Base):

    __tablename__ = 'user_access_tokens'

    user_id = Column('user_id', BigInteger,
                     ForeignKey('user.id', onupdate='cascade', ondelete='cascade'),
                     primary_key=True, nullable=False, unique=True)
    access_token = Column('access_token', BigInteger, nullable=False, unique=True)

    # Delete records after an hour.
