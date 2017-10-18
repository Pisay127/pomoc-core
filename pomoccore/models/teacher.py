# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import BigInteger
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Teacher(BaseModel):

    __tablename__ = 'teacher_account'

    teacher_id = Column('id', BigInteger,
                        ForeignKey('user.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=True, unique=True)

    pending_subject_grades = relationship('StudentSubjectPendingGrade', backref='teacher_account')
    section_advisories = relationship('SectionAdvisor', backref='teacher_account')
    batch_advisories = relationship('BatchAdvisor', backref='teacher_account')
    subjects = relationship('SubjectOffering', backref='teacher_account')

    def __init__(self, teacher_id):
        self.teacher_id = teacher_id

    def __repr__(self):
        return '<Teacher {0}>'.format(self.teacher_id)


class TeacherPosition(BaseModel):

    __tablename__ = 'teacher_position'

    teacher_id = Column('teacher_id', BigInteger,
                        ForeignKey('teacher_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    position_id = Column('position_id', BigInteger,
                         ForeignKey('teacher_position_list.id', onupdate='cascade', ondelete='cascade'),
                         nullable=False)
    school_year = Column('school_year', Text, nullable=False)

    def __init__(self, teacher_id, position_name, school_year):
        self.teacher_id = teacher_id
        self.position_name = position_name
        self.school_year = school_year

    def __repr__(self):
        return '<TeacherPosition {0} - {1} ({2})'.format(self.teacher_id,
                                                         self.position_name,
                                                         self.school_year)


class TeacherPositionList(BaseModel):

    __tablename__ = 'teacher_position_list'

    position_id = Column('id', BigInteger, primary_key=True, unique=True, nullable=False, autoincrement=True)
    position_name = Column('position_name', Text, nullable=False)

    teachers = relationship('TeacherPosition', backref='teacher_position_list')

    def __init__(self, position_name):
        self.position_name = position_name

    def __repr__(self):
        return '<TeacherPositionList {0}>'.format(self.position_name)
