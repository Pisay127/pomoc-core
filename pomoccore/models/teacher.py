# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .user import UserModel


class Teacher(UserModel):

    __tablename__ = 'teacher_account'

    pending_subject_grades = relationship('StudentSubjectPendingGrade', backref='teacher_account')

    def __init__(self, id_number, username, password, first_name,
                 middle_name, last_name, age, birth_date, profile_picture=None):
        super(Teacher, self).__init__(id_number, username, password, first_name,
                                      middle_name, last_name, age, birth_date, profile_picture)

    def __repr__(self):
        return '<Teacher {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)


class TeacherPosition(BaseModel):

    __tablename__ = 'teacher_position'

    teacher_id = Column('teacher_id', Text, primary_key=True, nullable=False)
    position_name = Column('position_name', Text, primary_key=True, nullable=False)
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

    position_name = Column('position_name', Text, primary_key=True, nullable=False)
    active = Column('active', Boolean, nullable=False)

    def __init__(self, position_name, active=True):
        self.position_name = position_name
        self.active = active

    def __repr__(self):
        return '<TeacherPositionList {0} ({1})>'.format(self.position_name,
                                                        'active' if self.active else 'inactive')
