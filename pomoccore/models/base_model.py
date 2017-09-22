# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base


class Base(object):

    __abstract__ = True
    date_created = Column('date_created', DateTime, default=func.current_timestamp(), nullable=False)
    date_modified = Column('date_modified', DateTime, default=func.current_timestamp(),
                           onupdate=func.current_timestamp(), nullable=False)

BaseModel = declarative_base(cls=Base)
