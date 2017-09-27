# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import SmallInteger
from sqlalchemy import Text
from sqlalchemy.schema import ForeignKeyConstraint

from .base_model import BaseModel
from .user import UserModel


class Student(UserModel):

    __tablename__ = 'student_account'

    year_level = Column('year_level', SmallInteger, nullable=False)

    def __init__(self, id_number, username, password, first_name,
                 middle_name, last_name, age, birth_date, year_level,
                 profile_picture=None):
        super(Student, self).__init__(id_number, username, password, first_name,
                                      middle_name, last_name, age, birth_date, profile_picture)
        self.year_level = year_level

    def __repr__(self):
        return '<Student {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)


class StudentMonthlyRequiredDays(BaseModel):

    __tablename__ = 'student_monthly_required_days'

    month = Column('month', SmallInteger, primary_key=True, nullable=False)
    days_required = Column('days_required', SmallInteger, nullable=True)

    def __init__(self, month, days_required):
        self.month = month
        self.days_required = days_required

    def __repr__(self):
        return '<StudentMonthlyRequiredDays {0}'.format(self.month)


class StudentMonthlyAttendance(BaseModel):

    __tablename__ = 'student_monthly_attendance'
    __table_args__ = (ForeignKeyConstraint(['student_number'], ['student_account.id_number']))

    student_number = Column('student_number', Text, primary_key=True, nullable=False)
    month = Column('month', SmallInteger, primary_key=True, nullable=False)
    quarter = Column('quarter', SmallInteger, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)
    school_year = Column('school_year', Text, nullable=False)
    days_required = Column('days_required', SmallInteger, nullable=False)
    days_present = Column('days_present', SmallInteger, nullable=False)
    days_tardy = Column('days_tardy', SmallInteger, nullable=False)
    days_absent = Column('days_absent', SmallInteger, nullable=False)

    def __init__(self, student_number, month, quarter, year_level,
                 school_year, days_required, days_present, days_tardy, days_absent):
        self.student_number = student_number
        self.month = month
        self.quarter = quarter
        self.year_level = year_level
        self.school_year = school_year
        self.days_required = days_required
        self.days_present = days_present
        self.days_tardy = days_tardy
        self.days_absent = days_absent

    def __repr__(self):
        return '<StudentMonthlyAttendance {0} - Month {1}>'.format(self.student_number, self.month)


class StudentStatus(BaseModel):

    __tablename__ = 'student_status'
    __table_args__ = (ForeignKeyConstraint(['student_number'], ['student_account.id_number']))

    student_number = Column('student_number', Text, primary_key=True, nullable=False)
    status = Column('status', Text, primary_key=True, nullable=False)
    quarter = Column('quarter', SmallInteger, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)

    def __init__(self, student_number, status, quarter, year_level, school_year):
        self.student_number = student_number
        self.status = status
        self.quarter = quarter
        self.year_level = year_level
        self.school_year = school_year

    def __repr__(self):
        return '<StudentStatus {0} - {1}>'.format(self.student_number, self.quarter)
