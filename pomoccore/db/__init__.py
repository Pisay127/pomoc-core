# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from pomoccore import settings

db_engine = create_engine(settings.DB_URL, **settings.DB_OPTIONS)
session_factory = sessionmaker(bind=db_engine)
Session = scoped_session(session_factory)


def init_db():
    Session.configure(bind=db_engine)

    from pomoccore.models.base_model import BaseModel
    from pomoccore.models.user import UserModel

    # noinspection PyUnresolvedReferences
    from pomoccore.models.student import Student

    # noinspection PyUnresolvedReferences
    from pomoccore.models.teacher import Teacher

    # noinspection PyUnresolvedReferences
    from pomoccore.models.admin import Admin

    BaseModel.metadata.create_all(db_engine)
    UserModel.metadata.create_all(db_engine)
