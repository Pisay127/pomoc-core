# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Base(BaseModel):

    __abstract__ = True
    date_created = Column(DateTime, default="")  # Set default to current_timestamp()
    date_modified = Column(DateTime, default="", onupdate="")  # Set default and onupdate to current_timestamp()
