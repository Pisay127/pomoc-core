# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

from sqlalchemy import Column
from sqlalchemy import SmallInteger
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import CHAR
from sqlalchemy import DECIMAL
from sqlalchemy.schema import ForeignKey
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .user import UserModel


class Student(UserModel):

    __tablename__ = 'student_account'

    year_level = Column('year_level', SmallInteger, nullable=False)

    sections = relationship('StudentSection', backref='student_account')
    ratings = relationship('StudentRating', backref='student_account')
    batch = relationship('StudentBatch', backref='student_account', uselist=False)
    monthly_attendance = relationship('StudentMonthlyAttendance', backref='student_account')
    statuses = relationship('StudentStatus', backref='student_account')
    subjects = relationship('StudentSubject', backref='student_account')
    subject_grades = relationship('StudentSubjectGrade', backref='student_account')
    pending_subject_grades = relationship('StudentSubjectPendingGrade', backref='student_account')

    def __init__(self, id_number, username, password, first_name,
                 middle_name, last_name, age, birth_date, year_level,
                 profile_picture=None):
        super(Student, self).__init__(id_number, username, password, first_name,
                                      middle_name, last_name, age, birth_date, profile_picture)
        self.year_level = year_level

    def __repr__(self):
        return '<Student {0}, a.k.a. {1}>'.format(self.id_number, self.user.username)


class StudentSection(BaseModel):

    __tablename__ = 'student_section'
    __table_args__ = (ForeignKeyConstraint(['section_name', 'year_level'],
                                           ['section.section_name', 'section.year_level']),)

    student_id = Column('student_id', Text,
                        ForeignKey('student_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    section_name = Column('section_name', Text,
                          ForeignKey('section.section_name', onupdate='cascade', ondelete='cascade'),
                          primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger,
                        ForeignKey('section.year_level', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=True)

    def __init__(self, student_id, section_name, year_level, school_year):
        self.student_id = student_id
        self.section_name = section_name
        self.year_level = year_level
        self.school_year = school_year

    def __repr__(self):
        return '<StudentSection {0}>'.format(self.section_name)


class StudentRating(BaseModel):

    __tablename__ = 'student_rating'

    student_id = Column('student_id', Text,
                        ForeignKey('student_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    criterion_id = Column('criterion_id', SmallInteger,
                          ForeignKey('student_character_rating_criteria', onupdate='cascade', ondelete='cascade'),
                          primary_key=True, nullable=False) 
    rating = Column('rating', CHAR, nullable=False)
    quarter = Column('quarter', SmallInteger, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)

    def __init__(self, student_id, criterion_id, rating, quarter, year_level, school_year):
        self.student_id = student_id
        self.criterion_id = criterion_id
        self.rating = rating
        self.quarter = quarter
        self.year_level = year_level
        self.school_year = school_year

    def __repr__(self):
        return '<StudentRating {0} - {1}'.format(self.student_id, self.criterion_id)


class StudentCharacterRatingCriteria(BaseModel):

    __tablename__ = 'student_character_rating_criteria'

    criterion_id = Column('criterion_id', SmallInteger, primary_key=True, nullable=False)
    criterion_description = Column('criterion_description', Text, primary_key=True, nullable=False)

    students = relationship('StudentRating', backref='student_character_rating_criteria')

    def __init__(self, criterion_id, criterion_description):
        self.criterion_id = criterion_id
        self.criterion_description = criterion_description

    def __repr__(self):
        return '<StudentCharacterRatingCriteria {0}'.format(self.criterion_id)


class StudentBatch(BaseModel):

    __tablename__ = 'student_batch'

    student_id = Column('student_id', Text,
                        ForeignKey('student_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    batch_year = Column('batch_year', Integer,
                        ForeignKey('batch.batch_year', onupdate='cascade', ondelete='cascade'),
                        nullable=False)

    def __init__(self, student_id, batch_year):
        self.student_id = student_id
        self.batch_year = batch_year

    def __repr__(self):
        return '<StudentBatch {0}>'.format(self.batch_year)


class StudentMonthlyRequiredDays(BaseModel):

    __tablename__ = 'student_monthly_required_days'

    month = Column('month', SmallInteger, primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)
    days_required = Column('days_required', SmallInteger, nullable=True)

    def __init__(self, month, days_required):
        self.month = month
        self.days_required = days_required

    def __repr__(self):
        return '<StudentMonthlyRequiredDays {0}'.format(self.month)


class StudentMonthlyAttendance(BaseModel):

    __tablename__ = 'student_monthly_attendance'
    __table_args__ = (ForeignKeyConstraint(['month', 'school_year'],
                                           ['student_monthly_required_days.month',
                                            'student_monthly_required_days.school_year']),)

    student_id = Column('student_id', Text,
                        ForeignKey('student_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    month = Column('month', SmallInteger,
                   ForeignKey('student_monthly_required_days.month', onupdate='cascade', ondelete='cascade'),
                   primary_key=True, nullable=False)
    quarter = Column('quarter', SmallInteger, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)
    school_year = Column('school_year', Text,
                         ForeignKey('student_monthly_required_days.month', onupdate='cascade', ondelete='cascade'),
                         nullable=False)
    days_required = Column('days_required', SmallInteger, nullable=False)
    days_present = Column('days_present', SmallInteger, nullable=False)
    days_tardy = Column('days_tardy', SmallInteger, nullable=False)
    days_absent = Column('days_absent', SmallInteger, nullable=False)

    def __init__(self, student_id, month, quarter, year_level,
                 school_year, days_required, days_present, days_tardy, days_absent):
        self.student_id = student_id
        self.month = month
        self.quarter = quarter
        self.year_level = year_level
        self.school_year = school_year
        self.days_required = days_required
        self.days_present = days_present
        self.days_tardy = days_tardy
        self.days_absent = days_absent

    def __repr__(self):
        return '<StudentMonthlyAttendance {0} - Month {1}>'.format(self.student_id, self.month)


class StudentStatus(BaseModel):

    __tablename__ = 'student_status'

    student_id = Column('student_id', Text,
                        ForeignKey('student_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    status = Column('status', Text, primary_key=True, nullable=False)
    quarter = Column('quarter', SmallInteger, primary_key=True, nullable=False)
    year_level = Column('year_level', SmallInteger, primary_key=True, nullable=False)
    school_year = Column('school_year', Text, primary_key=True, nullable=False)

    def __init__(self, student_id, status, quarter, year_level, school_year):
        self.student_id = student_id
        self.status = status
        self.quarter = quarter
        self.year_level = year_level
        self.school_year = school_year

    def __repr__(self):
        return '<StudentStatus {0} - {1}>'.format(self.student_id, self.quarter)


class StudentSubject(BaseModel):

    __tablename__ = 'student_subject'
    __table_args__ = (ForeignKeyConstraint(['subject_name', 'school_year', 'instructor'],
                                           ['subject_offering.subject_name',
                                            'subject_offering.school_year',
                                            'subject_offering.instructor']),)

    student_id = Column('student_id', Text,
                        ForeignKey('student_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    subject_name = Column('student_name', Text,
                          ForeignKey('subject_offering.subject_name', onupdate='cascade', ondelete='cascade'),
                          primary_key=True, nullable=False)
    school_year = Column('school_year', Text,
                         ForeignKey('subject_offering.school_year', onupdate='cascade', ondelete='cascade'),
                         primary_key=True, nullable=False)
    instructor = Column('instructor', Text,
                        ForeignKey('subject_offering.instructor', onupdate='cascade', ondelete='cascade'),
                        nullable=False)

    subject_grades = relationship('StudentSubjectGrade', backref='student_subject')

    def __init__(self, student_id, subject_name, school_year, instructor):
        self.student_id = student_id
        self.subject_name = subject_name
        self.school_year = school_year
        self.instructor = instructor

    def __repr__(self):
        return '<StudentSubject {0} - {1}'.format(self.subject_name, self.student_id)


class StudentSubjectGrade(BaseModel):

    __tablename__ = 'student_subject_grade'
    __table_args__ = (ForeignKeyConstraint(['subject_name', 'school_year'],
                                           ['student_subject.subject_name', 'student_subject.school_year']),)

    student_id = Column('student_id', Text, primary_key=True, nullable=False)
    subject_name = Column('subject_name', Text,
                          ForeignKey('student_subject.subject_name', onupdate='cascade', ondelete='cascade'),
                          primary_key=True, nullable=False)
    school_year = Column('school_year', Text,
                         ForeignKey('student_subject.school_year', onupdate='cascade', ondelete='cascade'),
                         primary_key=True, nullable=False)
    quarter = Column('quarter', SmallInteger, primary_key=True, nullable=False)
    grade = Column('grade', DECIMAL, nullable=False)

    pending_grades = relationship('StudentSubjectPendingGrade', backref='student_subject_grade',
                                  uselist=False)

    def __init__(self, student_id, subject_name, school_year, quarter, grade):
        self.student_id = student_id
        self.subject_name = subject_name
        self.school_year = school_year
        self.quarter = quarter
        self.grade = grade

    def __repr__(self):
        return '<StudentSubjectGrade {0} ({1}) - {2}'.format(self.subject_name, self.grade, self.student_id)


class StudentSubjectPendingGrade(BaseModel):

    __tablename__ = 'student_subject_pending_grade'
    __table_args__ = (ForeignKeyConstraint(['subject_name', 'school_year', 'quarter'],
                                           ['student_subject_grade.subject_name',
                                            'student_subject_grade.school_year',
                                            'student_subject_grade.quarter']),)

    student_id = Column('student_id', Text,
                        ForeignKey('student_account.id', onupdate='cascade', ondelete='cascade'),
                        primary_key=True, nullable=False)
    subject_name = Column('subject_name', Text,
                          ForeignKey('student_subject_grade.subject_name', onupdate='cascade', ondelete='cascade'),
                          primary_key=True, nullable=False)
    requesting_teacher = Column('requesting_teacher', Text,
                                ForeignKey('teacher_account.id', onupdate='cascade', ondelete='cascade'),
                                nullable=False)
    school_year = Column('school_year', Text,
                         ForeignKey('student_subject_grade.school_year', onupdate='cascade', ondelete='cascade'),
                         primary_key=True, nullable=False)
    quarter = Column('quarter', SmallInteger,
                     ForeignKey('student_subject_grade.quarter', onupdate='cascade', ondelete='cascade'),
                     primary_key=True, nullable=False)
    proposed_grade = Column('proposed_grade', DECIMAL, nullable=False)

    def __init__(self, student_id, subject_name, requesting_teacher, school_year, quarter, proposed_quarter):
        self.student_id = student_id
        self.subject_name = subject_name
        self.requesting_teacher = requesting_teacher
        self.school_year = school_year
        self.quarter = quarter
        self.proposed_grade = proposed_quarter

    def __repr__(self):
        return '<StudentSubjectPendingGrade {0} (*{1}) - {2}>'.format(self.subject_name,
                                                                             self.proposed_grade,
                                                                             self.student_id)
