from django.urls import path

from .views import (
    student_register,
    teacher_register,
    login_view,
    student_dashboard,
    teacher_dashboard,
    admin_dashboard,
)

from academy.views import student_exams


urlpatterns = [

    # تسجيل الطالب
    path(
        "register/student/",
        student_register,
        name="student_register"
    ),

    # تسجيل المعلم
    path(
        "register/teacher/",
        teacher_register,
        name="teacher_register"
    ),

    # تسجيل الدخول
    path(
        "login/",
        login_view,
        name="login"
    ),

    # لوحات التحكم
    path(
        "dashboard/student/",
        student_dashboard,
        name="student_dashboard"
    ),

    path(
        "dashboard/teacher/",
        teacher_dashboard,
        name="teacher_dashboard"
    ),

    path(
        "dashboard/admin/",
        admin_dashboard,
        name="admin_dashboard"
    ),

    # اختبارات الطالب
    path(
        "dashboard/exams/",
        student_exams,
        name="student_exams"
    ),
]