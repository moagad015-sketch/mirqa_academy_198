from django.urls import path

from .views import (
    home,

    # الطلاب
    student_list,
    student_detail,
    assign_student_teacher,

    # طلبات التسجيل
    registration_requests,
    registration_request_detail,
    approve_registration,
    reject_registration,

    # الإعدادات
    site_settings,

    # المعلمون
    teacher_list,
    teacher_detail,

    # الدورات
    course_list,
    course_create,
    course_edit,
    course_delete,

    # الدروس
    lesson_list,
    lesson_create,
    lesson_edit,
    lesson_delete,

    # الإعلانات
    announcement_list,
    announcement_create,
    announcement_edit,
    announcement_delete,

    # الشهادات
    certificate_list,
    certificate_create,
    certificate_edit,
    certificate_delete,
    certificate_verify,

    # الاختبارات
    exam_list,
    exam_create,
    exam_edit,
    exam_delete,
    exam_results,
    exam_attempt_grade,

    # بنك الأسئلة
    question_list,
    question_create,
    question_edit,
    question_delete,

    # اختيارات الأسئلة
    choice_create,
    choice_delete,

    # أقسام الاختبارات
    exam_section_list,
    exam_section_create,

    # أسئلة الاختبارات
    exam_question_list,
    exam_question_add,
    exam_question_delete,

    # اختبارات الطلاب
    exam_start,
    exam_take,
    exam_submit,
    exam_result,
)


urlpatterns = [

    # =========================
    # الصفحة الرئيسية
    # =========================

    path(
        "",
        home,
        name="home"
    ),

    # =========================
    # طلبات تسجيل الطلاب والمعلمين
    # =========================

    path(
        "dashboard/registration-requests/",
        registration_requests,
        name="registration_requests"
    ),

    path(
        "dashboard/registration-requests/<str:request_type>/<int:profile_id>/",
        registration_request_detail,
        name="registration_request_detail"
    ),

    path(
        "dashboard/registration-requests/<str:request_type>/<int:profile_id>/approve/",
        approve_registration,
        name="approve_registration"
    ),

    path(
        "dashboard/registration-requests/<str:request_type>/<int:profile_id>/reject/",
        reject_registration,
        name="reject_registration"
    ),

    # =========================
    # الطلاب
    # =========================

    path(
        "dashboard/students/",
        student_list,
        name="student_list"
    ),

    path(
        "dashboard/students/<int:student_id>/",
        student_detail,
        name="student_detail"
    ),

    path(
        "dashboard/students/<int:student_id>/assign-teacher/",
        assign_student_teacher,
        name="assign_student_teacher"
    ),

    # =========================
    # إعدادات الأكاديمية
    # =========================

    path(
        "dashboard/settings/",
        site_settings,
        name="site_settings"
    ),

    # =========================
    # المعلمون
    # =========================

    path(
        "dashboard/teachers/",
        teacher_list,
        name="teacher_list"
    ),

    path(
        "dashboard/teachers/<int:teacher_id>/",
        teacher_detail,
        name="teacher_detail"
    ),

    # =========================
    # الدورات
    # =========================

    path(
        "dashboard/courses/",
        course_list,
        name="course_list"
    ),

    path(
        "dashboard/courses/add/",
        course_create,
        name="course_create"
    ),

    path(
        "dashboard/courses/edit/<int:course_id>/",
        course_edit,
        name="course_edit"
    ),

    path(
        "dashboard/courses/delete/<int:course_id>/",
        course_delete,
        name="course_delete"
    ),

    # =========================
    # الدروس
    # =========================

    path(
        "dashboard/courses/<int:course_id>/lessons/",
        lesson_list,
        name="lesson_list"
    ),

    path(
        "dashboard/courses/<int:course_id>/lessons/add/",
        lesson_create,
        name="lesson_create"
    ),

    path(
        "dashboard/lessons/edit/<int:lesson_id>/",
        lesson_edit,
        name="lesson_edit"
    ),

    path(
        "dashboard/lessons/delete/<int:lesson_id>/",
        lesson_delete,
        name="lesson_delete"
    ),

    # =========================
    # الإعلانات
    # =========================

    path(
        "dashboard/announcements/",
        announcement_list,
        name="announcement_list"
    ),

    path(
        "dashboard/announcements/add/",
        announcement_create,
        name="announcement_create"
    ),

    path(
        "dashboard/announcements/edit/<int:announcement_id>/",
        announcement_edit,
        name="announcement_edit"
    ),

    path(
        "dashboard/announcements/delete/<int:announcement_id>/",
        announcement_delete,
        name="announcement_delete"
    ),

    # =========================
    # الشهادات
    # =========================

    path(
        "dashboard/certificates/",
        certificate_list,
        name="certificate_list"
    ),

    path(
        "dashboard/certificates/add/",
        certificate_create,
        name="certificate_create"
    ),

    path(
        "dashboard/certificates/edit/<int:certificate_id>/",
        certificate_edit,
        name="certificate_edit"
    ),

    path(
        "dashboard/certificates/delete/<int:certificate_id>/",
        certificate_delete,
        name="certificate_delete"
    ),

    path(
        "certificate/verify/<str:certificate_number>/",
        certificate_verify,
        name="certificate_verify"
    ),

    # =========================
    # إدارة الاختبارات
    # =========================

    path(
        "dashboard/exams/",
        exam_list,
        name="exam_list"
    ),

    path(
        "dashboard/exams/create/",
        exam_create,
        name="exam_create"
    ),

    path(
        "dashboard/exams/<int:exam_id>/edit/",
        exam_edit,
        name="exam_edit"
    ),

    path(
        "dashboard/exams/<int:exam_id>/delete/",
        exam_delete,
        name="exam_delete"
    ),

    # =========================
    # أقسام الاختبار
    # =========================

    path(
        "dashboard/exams/<int:exam_id>/sections/",
        exam_section_list,
        name="exam_section_list"
    ),

    path(
        "dashboard/exams/<int:exam_id>/sections/add/",
        exam_section_create,
        name="exam_section_create"
    ),

    # =========================
    # أسئلة الاختبار
    # =========================

    path(
        "dashboard/exams/<int:exam_id>/questions/",
        exam_question_list,
        name="exam_question_list"
    ),

    path(
        "dashboard/exams/<int:exam_id>/questions/add/",
        exam_question_add,
        name="exam_question_add"
    ),

    path(
        "dashboard/exam-questions/<int:exam_question_id>/delete/",
        exam_question_delete,
        name="exam_question_delete"
    ),

    # =========================
    # بنك الأسئلة
    # =========================

    path(
        "dashboard/questions/",
        question_list,
        name="question_list"
    ),

    path(
        "dashboard/questions/add/",
        question_create,
        name="question_create"
    ),

    path(
        "dashboard/questions/edit/<int:question_id>/",
        question_edit,
        name="question_edit"
    ),

    path(
        "dashboard/questions/delete/<int:question_id>/",
        question_delete,
        name="question_delete"
    ),

    # =========================
    # اختيارات الأسئلة
    # =========================

    path(
        "dashboard/questions/<int:question_id>/choices/add/",
        choice_create,
        name="choice_create"
    ),

    path(
        "dashboard/questions/choices/delete/<int:choice_id>/",
        choice_delete,
        name="choice_delete"
    ),

    # =========================
    # اختبارات الطلاب
    # =========================

    path(
        "dashboard/exams/<int:exam_id>/start/",
        exam_start,
        name="exam_start"
    ),

    path(
        "dashboard/exams/<int:exam_id>/take/",
        exam_take,
        name="exam_take"
    ),

    path(
        "dashboard/exams/<int:exam_id>/submit/",
        exam_submit,
        name="exam_submit"
    ),

    path(
        "dashboard/exams/<int:exam_id>/result/<int:attempt_id>/",
        exam_result,
        name="exam_result"
    ),

    # =========================
    # نتائج الاختبارات - الإدارة
    # =========================

    path(
        "dashboard/exams/<int:exam_id>/results/",
        exam_results,
        name="exam_results"
    ),

    path(
        "dashboard/exams/<int:exam_id>/results/<int:attempt_id>/grade/",
        exam_attempt_grade,
        name="exam_attempt_grade"
    ),
]