# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import falcon

from pomoccore.controllers import admin_controller
from pomoccore.controllers import batch_controller
from pomoccore.controllers import client_app_controller
from pomoccore.controllers import misc_controller
from pomoccore.controllers import oauth_controller
from pomoccore.controllers import section_controller
from pomoccore.controllers import student_controller
from pomoccore.controllers import subject_controller
from pomoccore.controllers import teacher_controller
from pomoccore.controllers import user_controller


class API(falcon.API):
    def __init__(self, *args, **kwargs):
        super(API, self).__init__(*args, **kwargs)

        self.add_route('/admin', admin_controller.AdminController())
        self.add_route('/batch', batch_controller.BatchController())
        self.add_route('/batch/advisor/year', batch_controller.BatchAdvisorByYearController())
        self.add_route('/batch/advisor', batch_controller.BatchAdvisorController())
        self.add_route('/client_app', client_app_controller.ClientAppController())
        self.add_route('/settings', misc_controller.VariableSettingsController())
        self.add_route('/oauth', oauth_controller.OAuthController())
        self.add_route('/section', section_controller.SectionController())
        self.add_route('/section/advisor/year', section_controller.SectionAdvisorByYearController())
        self.add_route('/section/advisor', section_controller.SectionAdvisorController())
        self.add_route('/student', student_controller.StudentController())
        self.add_route('/student/section', student_controller.StudentSectionController())
        self.add_route('/student/gwa', student_controller.StudentGWAController())
        self.add_route('/student/rating', student_controller.StudentRatingController())
        self.add_route('/student/rating/criteria', student_controller.StudentRatingCriteriaController())
        self.add_route('/student/batch', student_controller.StudentBatchController())
        self.add_route('/student/requireddays', student_controller.StudentMonthlyRequiredDaysController())
        self.add_route('/student/attendance', student_controller.StudentMonthlyAttendanceController())
        self.add_route('/student/status', student_controller.StudentStatusController())
        self.add_route('/student/subject', student_controller.StudentSubjectController())
        self.add_route('/student/subject/grade', student_controller.StudentSubjectGradeController())
        self.add_route('/student/subject/grade/pending', student_controller.StudentSubjectPendingGradeController())
        self.add_route('/subject', subject_controller.SubjectController())
        self.add_route('/subject/offering', subject_controller.SubjectOfferingController())
        self.add_route('/teacher', teacher_controller.TeacherController())
        self.add_route('/teacher/position', teacher_controller.TeacherPositionController())
        self.add_route('/teacher/position/list', teacher_controller.TeacherPositionListController())
        self.add_route('/user', user_controller.UserController())