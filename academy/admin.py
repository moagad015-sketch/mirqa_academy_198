from django.contrib import admin
from .models import (
    StudentProfile,
    TeacherProfile,
    Course,
    Lesson,
    Enrollment,
    Certificate,
)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "age", "phone", "created_at")
    search_fields = ("user__username", "user__email", "phone")


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "created_at")
    search_fields = ("user__username", "user__email", "phone")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    search_fields = ("title", "description")
    list_filter = ("is_active",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active", "course")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "progress", "enrolled_at")
    list_filter = ("course",)
    search_fields = ("student__username", "course__title")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        "certificate_number",
        "student",
        "course",
        "issued_at",
    )
    search_fields = (
        "certificate_number",
        "student__username",
        "course__title",
    )