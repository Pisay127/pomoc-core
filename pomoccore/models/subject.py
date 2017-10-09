# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import Boolean
from sqlalchemy import BigInteger
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Subject(BaseModel):

    __tablename__ = 'subject'

    subject_id = Column('id', BigInteger, primary_key=True, nullable=True, autoincrement=True, unique=True)
    subject_name = Column('subject_name', Text, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)

    offerings = relationship('SubjectOffering', backref='subject')

    def __init__(self, subject_name, year_level):
        self.subject_name = subject_name
        self.year_level = year_level

    def __repr__(self):
        return '<Subject {0} - {1}>'.format(self.subject_id, self.subject_name)


class SubjectOffering(BaseModel):

    __tablename__ = 'subject_offering'
    __table_args__ = (ForeignKeyConstraint(['subject_id', 'year_level'],
                                           ['subject.id', 'subject.year_level']),)

    subject_id = Column('subject_id', Text,
                        ForeignKey('subject.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger,
                        ForeignKey('subject.year_level', onupdate='cascade', ondelete='cascade'),
                        nullable=False)
    instructor_id = Column('instructor_id', Text,
                           ForeignKey('teacher_account.id'),
                           primary_key=True, nullable=False)
    schedule = Column('schedule', Text, nullable=False)

    students = relationship('StudentSubject', backref='subject_offering')

    def __init__(self, subject_name, school_year, year_level, instructor_id, schedule):
        self.subject_name = subject_name
        self.school_year = school_year
        self.year_level = year_level
        self.instructor_id = instructor_id
        self.schedule = schedule

    def __repr__(self):
        return '<SubjectOffering {0} {1} ({2}) - {3} ({4})'.format(self.subject_name,
                                                                   self.year_level,
                                                                   self.school_year,
                                                                   self.instructor_id,
                                                                   self.schedule)
