# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Subject(BaseModel):

    __tablename__ = 'subject'

    subject_name = Column('subject_name', Text, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)
    active = Column('active', Boolean, nullable=False)

    def __init__(self, subject_name, year_level, active):
        self.subject_name = subject_name
        self.year_level = year_level
        self.active = active

    def __repr__(self):
        return '<Subject {0} - {1} ({2})'.format(self.subject_name,
                                                 self.year_level,
                                                 'active' if self.active else 'inactive')


class SubjectOffering(BaseModel):

    __tablename__ = 'subject_offering'

    subject_name = Column('subject_name', Text, primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, nullable=False)
    instructor = Column('instructor', Text, primary_key=True, nullable=False)
    schedule = Column('schedule', Text, nullable=False)

    students = relationship('StudentSubject', backref='subject_offering')

    def __init__(self, subject_name, school_year, year_level, instructor, schedule):
        self.subject_name = subject_name
        self.school_year = school_year
        self.year_level = year_level
        self.instructor = instructor
        self.schedule = schedule

    def __repr__(self):
        return '<SubjectOffering {0} {1} ({2}) - {3} ({4})'.format(self.subject_name,
                                                                   self.year_level,
                                                                   self.school_year,
                                                                   self.instructor,
                                                                   self.schedule)
