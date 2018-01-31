# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import SmallInteger
from sqlalchemy import BigInteger
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Section(BaseModel):

    __tablename__ = 'section'

    section_id = Column('id', BigInteger, nullable=False, primary_key=True, autoincrement=True, unique=True)
    section_name = Column('section_name', Text, nullable=False, unique=True)
    year_level = Column('year_level', SmallInteger, nullable=False)

    students = relationship('StudentSection', backref='section')
    advisors = relationship('SectionAdvisor', backref='section')

    def __init__(self, section_name, year_level):
        self.section_name = section_name
        self.year_level = year_level

    def __repr__(self):
        return '<Section {0}'.format(self.section_name)


class SectionAdvisor(BaseModel):

    __tablename__ = 'section_advisor'

    section_id = Column('section_id', BigInteger,
                        ForeignKey('section.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)
    advisor = Column('advisor', BigInteger,
                     ForeignKey('teacher_account.id', onupdate='cascade', ondelete='cascade'),
                     nullable=False)

    def __init__(self, section_name, school_year, advisor):
        self.section_name = section_name
        self.school_year = school_year
        self.advisor = advisor

    def __repr__(self):
        return '<SectionAdvisor {0} - {1} (S.Y. {2})>'.format(self.advisor, self.section_id, self.school_year)


class Batch(BaseModel):

    __tablename__ = 'batch'

    batch_year = Column('batch_year', Integer, primary_key=True, nullable=False)

    students = relationship('StudentBatch', backref='batch')
    advisors = relationship('BatchAdvisor', backref='batch')

    def __init__(self, batch_year):
        self.batch_year = batch_year

    def __repr__(self):
        return '<Batch {0}>'.format(self.batch_year)


class BatchAdvisor(BaseModel):

    __tablename__ = 'batch_advisor'

    batch_year = Column('batch_year', Integer,
                        ForeignKey('batch.batch_year', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)
    advisor = Column('advisor_id', BigInteger,
                     ForeignKey('teacher_account.id', onupdate='cascade', ondelete='cascade'),
                     primary_key=True, nullable=False)

    def __init__(self, batch_year, school_year, advisor):
        self.batch_year = batch_year
        self.school_year = school_year
        self.advisor = advisor

    def __repr__(self):
        return '<BatchAdvisor {0} - {1} (S.Y. {2})'.format(self.advisor_Id, self.batch_year, self.school_year)
