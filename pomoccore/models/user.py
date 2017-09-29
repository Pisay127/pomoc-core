# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import DateTime
from sqlalchemy_utils.types import PasswordType
from sqlalchemy.ext.declarative import declarative_base

from pomoccore import settings

from .base_model import Base


class User(Base):

    __abstract__ = True

    id = Column('id', Text, primary_key=True, nullable=False, unique=True)
    username = Column('username', Text, nullable=False, unique=True)
    password = Column('password', PasswordType(schemes=settings.PASSWORD_SCHEMES), nullable=False)
    first_name = Column('first_name', Text, nullable=False)
    middle_name = Column('middle_name', Text, nullable=False)
    last_name = Column('last_name', Text, nullable=False)
    age = Column('age', SmallInteger, nullable=False)
    birth_date = Column('birth_date', DateTime, nullable=False)
    profile_picture = Column('profile_picture', Text, nullable=False, default='{directory to default image}')

    def __init__(self, id, username, password, first_name,
                 middle_name, last_name, age, birth_date, profile_picture=None):

        self.id = id.strip()
        self.username = username.strip().lower()
        self.password = password.strip()
        self.first_name = first_name.strip()
        self.middle_name = middle_name.strip()
        self.last_name = last_name.strip()
        self.age = age.strip()
        self.birth_date = birth_date  # Note to convert `birth_date` to something matches its type (DateTime)

        if profile_picture:
            self.profile_picture = profile_picture

UserModel = declarative_base(cls=User)
