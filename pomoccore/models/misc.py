# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import SmallInteger
from sqlalchemy import Text

from .base_model import BaseModel


class VariableSettings(BaseModel):

    __tablename__ = 'variable_settings'

    current_quarter = Column('current_quarter', SmallInteger, primary_key=True, nullable=False)
    current_school_year = Column('current_school_year', Text, primary_key=True, nullable=False)
    start_month = Column('start_month', SmallInteger, primary_key=True, nullable=False)
    end_month = Column('end_month', SmallInteger, primary_key=True, nullable=False)

    def __init__(self, current_quarter, current_school_year, start_month, end_month):
        self.current_quarter = current_quarter
        self.current_school_year = current_school_year
        self.start_month = start_month
        self.end_month = end_month

    def __repr__(self):
        return '<SystemWideInfo ({0}, {1}, {2}, {3})>'.format(self.current_quarter,
                                                              self.current_school_year,
                                                              self.start_month,
                                                              self.end_month)
