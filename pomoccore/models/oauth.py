# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import BigInteger
from sqlalchemy_utils import PasswordType
from sqlalchemy.schema import ForeignKey

from pomoccore import settings

from .base_model import BaseModel


class ClientApp(BaseModel):

    __tablename__ = 'client_app'

    app_id = Column('app_id', BigInteger, nullable=False, unique=True, primary_key=True)
    app_secret = Column('app_secret', PasswordType(schemes=settings.PASSWORD_SCHEMES), nullable=False)
    scope = Column('scope', Text, nullable=True)  # Nullable since scope is optional

    def __init__(self, app_id, app_secret, scope=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.scope = scope


class FirstPartyApp(BaseModel):

    __tablename__ = 'first_party_app'

    app_id = Column('app_id', BigInteger,
                    ForeignKey('client_app.app_id', onupdate='cascade', ondelete='cascade'),
                    primary_key=True, nullable=False, unique=True)

    def __init__(self, app_id):
        self.app_id = app_id


# class RefreshTokens()
# class BlackListedAccessTokens()