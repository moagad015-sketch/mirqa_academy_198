from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import StudentRegisterForm, TeacherRegisterForm

from academy.models import (
    Enrollment,
    Certificate,
    Announcement,
    ExamAttempt,
)


# ==========================================
# تسجيل الطالب
# ==========================================

def student_register(request):

    if request.method == "POST":

        form = StudentRegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            return render(
                request,
                "accounts/registration_pending.html",
                {
                    "user": user,
                    "user_type": "الطالب",
                }
            )

    else:

        form = StudentRegisterForm()

    return render(
        request,
        "accounts/student_register.html",
        {
            "form": form
        }
    )


# ==========================================
# تسجيل المعلم
# ==========================================

def teacher_register(request):

    if request.method == "POST":

        form = TeacherRegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save()

            return render(
                request,
                "accounts/registration_pending.html",
                {
                    "user": user,
                    "user_type": "المعلم",
                }
            )

    else:

        form = TeacherRegisterForm()

    return render(
        request,
        "accounts/teacher_register.html",
        {
            "form": form
        }
    )


# ==========================================
# تسجيل الدخول
# ==========================================

def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            # =========================
            # المدير
            # =========================

            if (
                user.role == "admin"
                or user.is_staff
                or user.is_superuser
            ):

                login(request, user)

                return redirect("admin_dashboard")


            # =========================
            # الطالب
            # =========================

            elif user.role == "student":

                if not hasattr(user, "student_profile"):

                    return render(
                        request,
                        "accounts/registration_pending.html",
                        {
                            "user": user,
                            "user_type": "الطالب",
                        }
                    )

                if user.student_profile.status != "approved":

                    return render(
                        request,
                        "accounts/registration_pending.html",
                        {
                            "user": user,
                            "user_type": "الطالب",
                        }
                    )

                login(request, user)

                return redirect("student_dashboard")


            # =========================
            # المعلم
            # =========================

            elif user.role == "teacher":

                if not hasattr(user, "teacher_profile"):

                    return render(
                        request,
                        "accounts/registration_pending.html",
                        {
                            "user": user,
                            "user_type": "المعلم",
                        }
                    )

                if user.teacher_profile.status != "approved":

                    return render(
                        request,
                        "accounts/registration_pending.html",
                        {
                            "user": user,
                            "user_type": "المعلم",
                        }
                    )

                login(request, user)

                return redirect("teacher_dashboard")


            # =========================
            # أي حساب غير معروف
            # =========================

            return redirect("home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


# ==========================================
# لوحة تحكم الطالب
# ==========================================

@login_required
def student_dashboard(request):

    # السماح للطلاب فقط
    if request.user.role != "student":

        return redirect("home")


    # التأكد من وجود ملف الطالب
    if not hasattr(request.user, "student_profile"):

        return redirect("home")


    # التأكد من قبول الطالب
    if request.user.student_profile.status != "approved":

        return redirect("home")


    # ==========================================
    # المعلم المسؤول عن الطالب
    # ==========================================

    student_profile = request.user.student_profile

    teacher = student_profile.teacher


    # ==========================================
    # الكورسات المسجل فيها الطالب
    # ==========================================

    enrollments = (
        Enrollment.objects
        .filter(student=request.user)
        .select_related("course")
        .prefetch_related("course__lessons")
        .order_by("-enrolled_at")
    )


    # ==========================================
    # الشهادات الخاصة بالطالب
    # ==========================================

    certificates = (
        Certificate.objects
        .filter(
            student=request.user,
            is_valid=True
        )
        .select_related("course")
        .order_by("-issued_at")
    )


    # ==========================================
    # الامتحانات والنتائج
    # ==========================================

    exam_attempts = (
        ExamAttempt.objects
        .filter(student=request.user)
        .select_related("exam", "exam__course")
        .order_by("-started_at")
    )


    # ==========================================
    # الإعلانات الخاصة بالطلاب
    # ==========================================

    announcements = (
        Announcement.objects
        .filter(
            is_active=True,
            show_to_students=True
        )
        .order_by("-created_at")[:10]
    )


    # ==========================================
    # حساب عدد الكورسات
    # ==========================================

    courses_count = enrollments.count()


    # ==========================================
    # حساب عدد الشهادات
    # ==========================================

    certificates_count = certificates.count()


    # ==========================================
    # حساب عدد الامتحانات
    # ==========================================

    exams_count = exam_attempts.count()


    # ==========================================
    # إرسال البيانات إلى لوحة الطالب
    # ==========================================

    return render(
        request,
        "accounts/dashboard/student.html",
        {
            "student": request.user,
            "student_profile": student_profile,

            "teacher": teacher,

            "enrollments": enrollments,

            "certificates": certificates,

            "exam_attempts": exam_attempts,

            "announcements": announcements,

            "courses_count": courses_count,

            "certificates_count": certificates_count,

            "exams_count": exams_count,
        }
    )


# ==========================================
# لوحة تحكم المعلم
# ==========================================

@login_required
def teacher_dashboard(request):

    # السماح للمعلمين فقط
    if request.user.role != "teacher":

        return redirect("home")


    # التأكد من وجود ملف المعلم
    if not hasattr(request.user, "teacher_profile"):

        return redirect("home")


    # التأكد من قبول المعلم
    if request.user.teacher_profile.status != "approved":

        return redirect("home")


    # ==========================================
    # الطلاب التابعون للمعلم
    # ==========================================

    students = (
        request.user.teacher_profile.students
        .select_related("user")
        .order_by("-created_at")
    )


    # ==========================================
    # عدد الطلاب
    # ==========================================

    students_count = students.count()


    # ==========================================
    # الإعلانات الخاصة بالمعلمين
    # ==========================================

    announcements = (
        Announcement.objects
        .filter(
            is_active=True,
            show_to_teachers=True
        )
        .order_by("-created_at")[:10]
    )


    return render(
        request,
        "accounts/dashboard/teacher.html",
        {
            "teacher": request.user,
            "teacher_profile": request.user.teacher_profile,

            "students": students,

            "students_count": students_count,

            "announcements": announcements,
        }
    )


# ==========================================
# لوحة تحكم المدير
# ==========================================

@login_required
def admin_dashboard(request):

    # السماح للمدير الحقيقي فقط
    if not (
        request.user.role == "admin"
        or request.user.is_staff
        or request.user.is_superuser
    ):

        return redirect("home")


    return render(
        request,
        "dashboard/admin_dashboard.html"
    )