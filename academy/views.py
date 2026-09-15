from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import User

from .models import (
    StudentProfile,
    TeacherProfile,
    Course,
    Lesson,
    Announcement,
    Certificate,
    Exam,
    Question,
    Choice,
    ExamSection,
    ExamQuestion,
    ExamAttempt,
    Answer,
)

from .forms import (
    CourseForm,
    LessonForm,
    AnnouncementForm,
    CertificateForm,
    ExamForm,
    QuestionForm,
    ChoiceForm,
    DirectExamQuestionForm,
    AssignTeacherForm,
)


# =========================
# الصفحة الرئيسية
# =========================

def home(request):
    courses = Course.objects.filter(
        is_active=True
    ).order_by("-created_at")

    exams = Exam.objects.filter(
        status__in=[
            Exam.Status.PUBLISHED,
            Exam.Status.OPEN,
        ]
    ).select_related("course").order_by("-created_at")

    certificates = Certificate.objects.select_related(
        "student",
        "course"
    ).order_by("-issued_at")[:6]

    return render(
        request,
        "academy/home.html",
        {
            "courses": courses,
            "exams": exams,
            "certificates": certificates,
        }
    )


# =========================
# الطلاب
# =========================

@login_required
def student_list(request):

    if request.user.role != "admin":
        return redirect("home")

    students = User.objects.filter(
        role="student"
    ).order_by("-date_joined")

    return render(
        request,
        "dashboard/students/students_list.html",
        {
            "students": students
        }
    )


@login_required
def student_detail(request, student_id):

    if request.user.role != "admin":
        return redirect("home")

    student = get_object_or_404(
        User,
        id=student_id,
        role="student"
    )

    profile, created = StudentProfile.objects.get_or_create(
        user=student
    )

    return render(
        request,
        "dashboard/students/student_details.html",
        {
            "student": student,
            "profile": profile
        }
    )


# =========================
# المعلمون
# =========================

@login_required
def teacher_list(request):

    if request.user.role != "admin":
        return redirect("home")

    teachers = User.objects.filter(
        role="teacher"
    ).order_by("-date_joined")

    return render(
        request,
        "dashboard/teachers/teachers_list.html",
        {
            "teachers": teachers
        }
    )


@login_required
def teacher_detail(request, teacher_id):

    if request.user.role != "admin":
        return redirect("home")

    teacher = get_object_or_404(
        User,
        id=teacher_id,
        role="teacher"
    )

    profile, created = TeacherProfile.objects.get_or_create(
        user=teacher
    )

    return render(
        request,
        "dashboard/teachers/teacher_details.html",
        {
            "teacher": teacher,
            "profile": profile
        }
    )


# =========================
# الدورات
# =========================

@login_required
def course_list(request):

    if request.user.role != "admin":
        return redirect("home")

    courses = Course.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "dashboard/courses/course_list.html",
        {
            "courses": courses
        }
    )


@login_required
def course_create(request):

    if request.user.role != "admin":
        return redirect("home")

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                "course_list"
            )

    else:

        form = CourseForm()

    return render(
        request,
        "dashboard/courses/course_form.html",
        {
            "form": form
        }
    )


@login_required
def course_edit(request, course_id):

    if request.user.role != "admin":
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():

            form.save()

            return redirect(
                "course_list"
            )

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "dashboard/courses/course_form.html",
        {
            "form": form,
            "course": course
        }
    )


@login_required
def course_delete(request, course_id):

    if request.user.role != "admin":
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method == "POST":

        course.delete()

        return redirect(
            "course_list"
        )

    return render(
        request,
        "dashboard/courses/course_delete.html",
        {
            "course": course
        }
    )


# =========================
# دروس الدورات
# =========================

@login_required
def lesson_list(request, course_id):

    if request.user.role != "admin":
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id
    )

    lessons = course.lessons.all()

    return render(
        request,
        "dashboard/lessons/lesson_list.html",
        {
            "course": course,
            "lessons": lessons
        }
    )


@login_required
def lesson_create(request, course_id):

    if request.user.role != "admin":
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method == "POST":

        form = LessonForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            lesson = form.save(
                commit=False
            )

            lesson.course = course

            lesson.save()

            return redirect(
                "lesson_list",
                course_id=course.id
            )

    else:

        form = LessonForm()

    return render(
        request,
        "dashboard/lessons/lesson_form.html",
        {
            "form": form,
            "course": course
        }
    )


@login_required
def lesson_edit(request, lesson_id):

    if request.user.role != "admin":
        return redirect("home")

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    if request.method == "POST":

        form = LessonForm(
            request.POST,
            request.FILES,
            instance=lesson
        )

        if form.is_valid():

            form.save()

            return redirect(
                "lesson_list",
                course_id=lesson.course.id
            )

    else:

        form = LessonForm(
            instance=lesson
        )

    return render(
        request,
        "dashboard/lessons/lesson_form.html",
        {
            "form": form,
            "course": lesson.course,
            "lesson": lesson
        }
    )


@login_required
def lesson_delete(request, lesson_id):

    if request.user.role != "admin":
        return redirect("home")

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    course_id = lesson.course.id

    if request.method == "POST":

        lesson.delete()

        return redirect(
            "lesson_list",
            course_id=course_id
        )

    return render(
        request,
        "dashboard/lessons/lesson_delete.html",
        {
            "lesson": lesson
        }
    )


# =========================
# الإعلانات
# =========================

@login_required
def announcement_list(request):

    if request.user.role != "admin":
        return redirect("home")

    announcements = Announcement.objects.all()

    return render(
        request,
        "dashboard/announcements/announcement_list.html",
        {
            "announcements": announcements
        }
    )


@login_required
def announcement_create(request):

    if request.user.role != "admin":
        return redirect("home")

    if request.method == "POST":

        form = AnnouncementForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                "announcement_list"
            )

    else:

        form = AnnouncementForm()

    return render(
        request,
        "dashboard/announcements/announcement_form.html",
        {
            "form": form
        }
    )


@login_required
def announcement_edit(request, announcement_id):

    if request.user.role != "admin":
        return redirect("home")

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    if request.method == "POST":

        form = AnnouncementForm(
            request.POST,
            request.FILES,
            instance=announcement
        )

        if form.is_valid():

            form.save()

            return redirect(
                "announcement_list"
            )

    else:

        form = AnnouncementForm(
            instance=announcement
        )

    return render(
        request,
        "dashboard/announcements/announcement_form.html",
        {
            "form": form,
            "announcement": announcement
        }
    )


@login_required
def announcement_delete(request, announcement_id):

    if request.user.role != "admin":
        return redirect("home")

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    if request.method == "POST":

        announcement.delete()

        return redirect(
            "announcement_list"
        )

    return render(
        request,
        "dashboard/announcements/announcement_delete.html",
        {
            "announcement": announcement
        }
    )


# =========================
# الشهادات
# =========================

@login_required
def certificate_list(request):

    if request.user.role != "admin":
        return redirect("home")

    certificates = Certificate.objects.all().order_by(
        "-issued_at"
    )

    return render(
        request,
        "dashboard/certificates/certificate_list.html",
        {
            "certificates": certificates
        }
    )


@login_required
def certificate_create(request):

    if request.user.role != "admin":
        return redirect("home")

    if request.method == "POST":

        form = CertificateForm(
            request.POST
        )

        if form.is_valid():

            certificate = form.save(
                commit=False
            )

            if not certificate.certificate_number:

                certificate.certificate_number = (
                    "MRQ-"
                    + uuid.uuid4().hex[:10].upper()
                )

            certificate.save()

            return redirect(
                "certificate_list"
            )

    else:

        form = CertificateForm()

    return render(
        request,
        "dashboard/certificates/certificate_form.html",
        {
            "form": form
        }
    )


@login_required
def certificate_edit(request, certificate_id):

    if request.user.role != "admin":
        return redirect("home")

    certificate = get_object_or_404(
        Certificate,
        id=certificate_id
    )

    if request.method == "POST":

        form = CertificateForm(
            request.POST,
            instance=certificate
        )

        if form.is_valid():

            form.save()

            return redirect(
                "certificate_list"
            )

    else:

        form = CertificateForm(
            instance=certificate
        )

    return render(
        request,
        "dashboard/certificates/certificate_form.html",
        {
            "form": form,
            "certificate": certificate
        }
    )


@login_required
def certificate_delete(request, certificate_id):

    if request.user.role != "admin":
        return redirect("home")

    certificate = get_object_or_404(
        Certificate,
        id=certificate_id
    )

    if request.method == "POST":

        certificate.delete()

        return redirect(
            "certificate_list"
        )

    return render(
        request,
        "dashboard/certificates/certificate_delete.html",
        {
            "certificate": certificate
        }
    )


# =========================
# التحقق من الشهادة
# =========================

def certificate_verify(request, certificate_number):

    certificate = Certificate.objects.filter(
        certificate_number=certificate_number,
        is_valid=True
    ).first()

    return render(
        request,
        "certificate_verify.html",
        {
            "certificate": certificate,
            "certificate_number": certificate_number
        }
    )


# =========================
# الاختبارات
# =========================

@login_required
def exam_list(request):

    if request.user.role != "admin":
        return redirect("home")

    exams = Exam.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "dashboard/exams/exam_list.html",
        {
            "exams": exams
        }
    )


@login_required
def exam_create(request):

    if request.user.role != "admin":
        return redirect("home")

    if request.method == "POST":

        form = ExamForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "exam_list"
            )

    else:

        form = ExamForm()

    return render(
        request,
        "dashboard/exams/exam_form.html",
        {
            "form": form
        }
    )


@login_required
def exam_edit(request, exam_id):

    if request.user.role != "admin":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    if request.method == "POST":

        form = ExamForm(
            request.POST,
            instance=exam
        )

        if form.is_valid():

            form.save()

            return redirect(
                "exam_list"
            )

    else:

        form = ExamForm(
            instance=exam
        )

    return render(
        request,
        "dashboard/exams/exam_form.html",
        {
            "form": form,
            "exam": exam
        }
    )


@login_required
def exam_delete(request, exam_id):

    if request.user.role != "admin":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    if request.method == "POST":

        exam.delete()

        return redirect(
            "exam_list"
        )

    return render(
        request,
        "dashboard/exams/exam_delete.html",
        {
            "exam": exam
        }
    )


# =========================
# بنك الأسئلة
# =========================

@login_required
def question_list(request):

    if request.user.role != "admin":
        return redirect("home")

    questions = Question.objects.select_related(
        "course",
        "lesson"
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/questions/question_list.html",
        {
            "questions": questions
        }
    )


@login_required
def question_create(request):

    if request.user.role != "admin":
        return redirect("home")

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.save()

            return redirect(
                "question_edit",
                question_id=question.id
            )

    else:

        form = QuestionForm()

    return render(
        request,
        "dashboard/questions/question_form.html",
        {
            "form": form
        }
    )


@login_required
def question_edit(request, question_id):

    if request.user.role != "admin":
        return redirect("home")

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if request.method == "POST":

        form = QuestionForm(
            request.POST,
            instance=question
        )

        if form.is_valid():

            form.save()

            return redirect(
                "question_edit",
                question_id=question.id
            )

    else:

        form = QuestionForm(
            instance=question
        )

    choices = question.choices.all()

    return render(
        request,
        "dashboard/questions/question_form.html",
        {
            "form": form,
            "question": question,
            "choices": choices,
        }
    )


@login_required
def question_delete(request, question_id):

    if request.user.role != "admin":
        return redirect("home")

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if request.method == "POST":

        question.delete()

        return redirect(
            "question_list"
        )

    return render(
        request,
        "dashboard/questions/question_delete.html",
        {
            "question": question
        }
    )


# =========================
# اختيارات الأسئلة
# =========================

@login_required
def choice_create(request, question_id):

    if request.user.role != "admin":
        return redirect("home")

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if request.method == "POST":

        form = ChoiceForm(request.POST)

        if form.is_valid():

            choice = form.save(
                commit=False
            )

            choice.question = question

            choice.save()

            return redirect(
                "question_edit",
                question_id=question.id
            )

    else:

        form = ChoiceForm()

    return render(
        request,
        "dashboard/questions/choice_form.html",
        {
            "form": form,
            "question": question,
        }
    )


@login_required
def choice_delete(request, choice_id):

    if request.user.role != "admin":
        return redirect("home")

    choice = get_object_or_404(
        Choice,
        id=choice_id
    )

    question_id = choice.question.id

    if request.method == "POST":

        choice.delete()

        return redirect(
            "question_edit",
            question_id=question_id
        )

    return render(
        request,
        "dashboard/questions/choice_delete.html",
        {
            "choice": choice
        }
    )


# =========================
# أقسام الاختبارات
# =========================

@login_required
def exam_section_list(request, exam_id):

    if request.user.role != "admin":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    sections = exam.sections.all()

    return render(
        request,
        "dashboard/exams/sections/section_list.html",
        {
            "exam": exam,
            "sections": sections,
        }
    )


@login_required
def exam_section_create(request, exam_id):

    if request.user.role != "admin":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    if request.method == "POST":

        form = ExamSectionForm(request.POST)

        if form.is_valid():

            section = form.save(
                commit=False
            )

            section.exam = exam

            section.save()

            return redirect(
                "exam_section_list",
                exam_id=exam.id
            )

    else:

        form = ExamSectionForm()

    return render(
        request,
        "dashboard/exams/sections/section_form.html",
        {
            "form": form,
            "exam": exam,
        }
    )


# =========================
# ربط الأسئلة بالاختبار
# =========================

@login_required
def exam_question_list(request, exam_id):

    if request.user.role != "admin":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    exam_questions = exam.exam_questions.select_related(
        "question",
        "section"
    ).order_by("order")

    return render(
        request,
        "dashboard/exams/questions/exam_question_list.html",
        {
            "exam": exam,
            "exam_questions": exam_questions,
        }
    )


@login_required
def exam_question_add(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.user.role != "admin":
        return redirect("home")

    if request.method == "POST":
        form = DirectExamQuestionForm(
            request.POST,
            exam=exam
        )

        if form.is_valid():

            question = Question.objects.create(
                course=exam.course,
                text=form.cleaned_data["text"],
                question_type=form.cleaned_data["question_type"],
                points=form.cleaned_data["points"],
                is_active=True,
                allow_random=True,
            )

            choices_data = []

            if form.cleaned_data["question_type"] == "mcq":
                choices_data = [
                    form.cleaned_data.get("choice_1"),
                    form.cleaned_data.get("choice_2"),
                    form.cleaned_data.get("choice_3"),
                    form.cleaned_data.get("choice_4"),
                ]

            elif form.cleaned_data["question_type"] == "true_false":
                choices_data = [
                    "صح",
                    "خطأ",
                ]

            correct_choice = form.cleaned_data.get(
                "correct_choice"
            )

            for index, choice_text in enumerate(
                choices_data,
                start=1
            ):
                if choice_text:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=(
                            index == correct_choice
                        ),
                        order=index,
                    )

            ExamQuestion.objects.create(
                exam=exam,
                section=form.cleaned_data.get("section"),
                question=question,
                order=form.cleaned_data["order"],
                is_required=True,
            )

            return redirect(
                "exam_question_list",
                exam_id=exam.id
            )

    else:
        form = DirectExamQuestionForm(
            exam=exam
        )

    return render(
        request,
        "dashboard/exams/questions/exam_question_form.html",
        {
            "form": form,
            "exam": exam,
        }
    )


@login_required
def exam_question_delete(request, exam_question_id):

    if request.user.role != "admin":
        return redirect("home")

    exam_question = get_object_or_404(
        ExamQuestion,
        id=exam_question_id
    )

    exam_id = exam_question.exam.id

    if request.method == "POST":

        exam_question.delete()

        return redirect(
            "exam_question_list",
            exam_id=exam_id
        )

    return render(
        request,
        "dashboard/exams/questions/exam_question_delete.html",
        {
            "exam_question": exam_question
        }
    )
@login_required
def student_exams(request):

    exams = Exam.objects.filter(
        status__in=[
            Exam.Status.PUBLISHED,
            Exam.Status.OPEN,
        ]
    ).select_related(
        "course"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "accounts/student_exams.html",
        {
            "exams": exams,
        }
    )
# =========================================================
# الطالب - بدء الاختبار
# =========================================================

@login_required
def exam_start(request, exam_id):

    if request.user.role != "student":
        return redirect("home")

    exam = get_object_or_404(
        Exam.objects.select_related("course"),
        id=exam_id
    )

    # الاختبار يجب أن يكون منشورًا أو مفتوحًا
    if exam.status not in [
        Exam.Status.PUBLISHED,
        Exam.Status.OPEN,
    ]:
        return redirect("student_exams")

    now = timezone.now()

    # التحقق من موعد بداية الاختبار
    if exam.start_at and now < exam.start_at:
        return redirect("student_exams")

    # التحقق من موعد نهاية الاختبار
    if exam.end_at and now > exam.end_at:
        return redirect("student_exams")

    # عدد المحاولات السابقة
    attempts_count = ExamAttempt.objects.filter(
        exam=exam,
        student=request.user
    ).count()

    if attempts_count >= exam.max_attempts:
        return redirect("student_exams")

    # إذا كان للطالب محاولة قيد الحل نعيده إليها
    existing_attempt = ExamAttempt.objects.filter(
        exam=exam,
        student=request.user,
        status=ExamAttempt.Status.IN_PROGRESS
    ).first()

    if existing_attempt:
        return redirect(
            "exam_take",
            exam_id=exam.id
        )

    attempt_number = attempts_count + 1

    exam_questions = exam.exam_questions.select_related(
        "question"
    ).all()

    total_score = sum(
        question.get_points()
        for question in exam_questions
    )

    attempt = ExamAttempt.objects.create(
        exam=exam,
        student=request.user,
        attempt_number=attempt_number,
        total_score=total_score,
        status=ExamAttempt.Status.IN_PROGRESS,
    )

    return redirect(
        "exam_take",
        exam_id=exam.id
    )


# =========================================================
# الطالب - صفحة حل الاختبار
# =========================================================

@login_required
def exam_take(request, exam_id):

    if request.user.role != "student":
        return redirect("home")

    exam = get_object_or_404(
        Exam.objects.select_related("course"),
        id=exam_id
    )

    attempt = ExamAttempt.objects.filter(
        exam=exam,
        student=request.user,
        status=ExamAttempt.Status.IN_PROGRESS
    ).first()

    if not attempt:
        return redirect(
            "exam_start",
            exam_id=exam.id
        )

    now = timezone.now()

    # انتهاء وقت الاختبار العام
    if exam.end_at and now > exam.end_at:
        return redirect(
            "exam_submit",
            exam_id=exam.id
        )

    exam_questions = exam.exam_questions.select_related(
        "question"
    ).prefetch_related(
        "question__choices"
    ).all()

    return render(
        request,
        "accounts/exam_take.html",
        {
            "exam": exam,
            "attempt": attempt,
            "exam_questions": exam_questions,
        }
    )


# =========================================================
# الطالب - تسليم الاختبار والتصحيح
# =========================================================

@login_required
@transaction.atomic
def exam_submit(request, exam_id):

    if request.user.role != "student":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    attempt = get_object_or_404(
        ExamAttempt,
        exam=exam,
        student=request.user,
        status=ExamAttempt.Status.IN_PROGRESS
    )

    if request.method != "POST":
        return redirect(
            "exam_take",
            exam_id=exam.id
        )

    exam_questions = exam.exam_questions.select_related(
        "question"
    ).prefetch_related(
        "question__choices"
    ).all()

    score = 0
    has_manual_questions = False

    # حذف الإجابات القديمة لو الصفحة اتبعت أكثر من مرة
    attempt.answers.all().delete()

    for exam_question in exam_questions:

        question = exam_question.question

        field_name = f"question_{question.id}"

        selected_value = request.POST.get(field_name)

        # =========================================
        # اختيار من متعدد / صح وخطأ
        # =========================================

        if question.question_type in [
            Question.QuestionType.MCQ,
            Question.QuestionType.TRUE_FALSE,
        ]:

            if selected_value:

                try:
                    choice = question.choices.get(
                        id=int(selected_value)
                    )
                except (
                    ValueError,
                    TypeError,
                    Choice.DoesNotExist
                ):
                    choice = None

                if choice:

                    is_correct = choice.is_correct

                    awarded_points = (
                        exam_question.get_points()
                        if is_correct
                        else 0
                    )

                    Answer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_choice=choice,
                        awarded_points=awarded_points,
                        is_correct=is_correct,
                        is_manually_graded=False,
                    )

                    score += awarded_points

                else:

                    Answer.objects.create(
                        attempt=attempt,
                        question=question,
                        awarded_points=0,
                        is_correct=False,
                        is_manually_graded=False,
                    )

            else:

                Answer.objects.create(
                    attempt=attempt,
                    question=question,
                    awarded_points=0,
                    is_correct=False,
                    is_manually_graded=False,
                )

        # =========================================
        # السؤال المقالي
        # =========================================

        elif question.question_type == Question.QuestionType.ESSAY:

            text_answer = request.POST.get(
                field_name,
                ""
            ).strip()

            Answer.objects.create(
                attempt=attempt,
                question=question,
                text_answer=text_answer,
                awarded_points=0,
                is_correct=None,
                is_manually_graded=False,
            )

            has_manual_questions = True

        # =========================================
        # السؤال الصوتي
        # =========================================

        elif question.question_type == Question.QuestionType.AUDIO:

            has_manual_questions = True

    attempt.score = score
    attempt.submitted_at = timezone.now()

    # لو يوجد أسئلة تحتاج تصحيحًا يدويًا
    if has_manual_questions:

        attempt.status = ExamAttempt.Status.REVIEWING
        attempt.passed = None

    else:

        attempt.status = ExamAttempt.Status.GRADED

        if attempt.total_score > 0:

            percentage = (
                float(score) /
                float(attempt.total_score)
            ) * 100

            attempt.passed = (
                percentage >= exam.passing_score
            )

        else:

            attempt.passed = False

    attempt.save()

    return redirect(
        "exam_result",
        exam_id=exam.id,
        attempt_id=attempt.id
    )


# =========================================================
# الطالب - نتيجة الاختبار
# =========================================================

@login_required
def exam_result(request, exam_id, attempt_id):

    if request.user.role != "student":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    attempt = get_object_or_404(
        ExamAttempt.objects.prefetch_related(
            "answers__question",
            "answers__selected_choice",
        ),
        id=attempt_id,
        exam=exam,
        student=request.user
    )

    return render(
        request,
        "accounts/exam_result.html",
        {
            "exam": exam,
            "attempt": attempt,
        }
    )
# =========================================================
# نتائج الاختبار - للمعلم والمدير
# =========================================================

@login_required
def exam_results(request, exam_id):

    if request.user.role not in ["admin", "teacher"]:
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    attempts = ExamAttempt.objects.filter(
        exam=exam
    ).select_related(
        "student"
    ).order_by(
        "-started_at"
    )

    return render(
        request,
        "dashboard/exams/results/exam_results.html",
        {
            "exam": exam,
            "attempts": attempts,
        }
    )


# =========================================================
# تصحيح محاولة طالب
# =========================================================

@login_required
def exam_attempt_grade(request, exam_id, attempt_id):

    if request.user.role != "admin":
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    attempt = get_object_or_404(
        ExamAttempt.objects.select_related(
            "student",
            "exam"
        ).prefetch_related(
            "answers__question",
            "answers__selected_choice",
        ),
        id=attempt_id,
        exam=exam
    )

    if request.method == "POST":

        for answer in attempt.answers.all():

            question = answer.question

            if question.question_type == Question.QuestionType.ESSAY:

                field_name = f"answer_{answer.id}"

                points_value = request.POST.get(
                    field_name
                )

                try:
                    points = float(points_value)
                except (
                    ValueError,
                    TypeError
                ):
                    points = 0

                max_points = question.points

                if points < 0:
                    points = 0

                if points > max_points:
                    points = max_points

                answer.awarded_points = points
                answer.is_manually_graded = True
                answer.is_correct = (
                    points >= max_points
                    if max_points > 0
                    else False
                )

                answer.teacher_feedback = request.POST.get(
                    f"feedback_{answer.id}",
                    ""
                ).strip()

                answer.save()

        # إعادة حساب الدرجة
        total_score = sum(
            answer.awarded_points
            for answer in attempt.answers.all()
        )

        attempt.score = total_score

        if attempt.total_score > 0:

            percentage = (
                float(total_score)
                / float(attempt.total_score)
            ) * 100

            attempt.passed = (
                percentage >= exam.passing_score
            )

        else:

            attempt.passed = False

        attempt.status = ExamAttempt.Status.GRADED

        attempt.save()

        return redirect(
            "exam_results",
            exam_id=exam.id
        )

    return render(
        request,
        "dashboard/exams/results/exam_attempt_grade.html",
        {
            "exam": exam,
            "attempt": attempt,
        }
    )
# ==========================================
# إعدادات الأكاديمية
# ==========================================

@login_required
def site_settings(request):

    if request.user.role != "admin":
        return redirect("home")

    from .forms import SiteSettingsForm
    from .models import SiteSettings

    settings = SiteSettings.objects.first()

    if settings is None:
        settings = SiteSettings.objects.create()

    if request.method == "POST":

        form = SiteSettingsForm(
            request.POST,
            request.FILES,
            instance=settings
        )

        if form.is_valid():
            form.save()
            return redirect("site_settings")

    else:

        form = SiteSettingsForm(
            instance=settings
        )

    return render(
        request,
        "dashboard/site_settings.html",
        {
            "form": form,
            "settings": settings,
        }
    )
# =========================
# طلبات تسجيل الطلاب والمعلمين
# =========================

@login_required
def registration_requests(request):

    if request.user.role != "admin":
        return redirect("home")

    pending_students = StudentProfile.objects.filter(
        status=StudentProfile.Status.PENDING
    ).select_related("user").order_by("-created_at")

    pending_teachers = TeacherProfile.objects.filter(
        status=TeacherProfile.Status.PENDING
    ).select_related("user").order_by("-created_at")

    return render(
        request,
        "dashboard/registration/registration_requests.html",
        {
            "pending_students": pending_students,
            "pending_teachers": pending_teachers,
        }
    )


@login_required
def registration_request_detail(request, request_type, profile_id):

    if request.user.role != "admin":
        return redirect("home")

    if request_type == "student":

        profile = get_object_or_404(
            StudentProfile.objects.select_related("user"),
            id=profile_id
        )

        return render(
            request,
            "dashboard/registration/student_request_detail.html",
            {
                "profile": profile,
                "user": profile.user,
                "request_type": "student",
            }
        )

    elif request_type == "teacher":

        profile = get_object_or_404(
            TeacherProfile.objects.select_related("user"),
            id=profile_id
        )

        return render(
            request,
            "dashboard/registration/teacher_request_detail.html",
            {
                "profile": profile,
                "user": profile.user,
                "request_type": "teacher",
            }
        )

    return redirect("registration_requests")


@login_required
def approve_registration(request, request_type, profile_id):

    if request.user.role != "admin":
        return redirect("home")

    if request.method != "POST":
        return redirect("registration_requests")

    if request_type == "student":

        profile = get_object_or_404(
            StudentProfile,
            id=profile_id
        )

        profile.status = StudentProfile.Status.APPROVED
        profile.save()

    elif request_type == "teacher":

        profile = get_object_or_404(
            TeacherProfile,
            id=profile_id
        )

        profile.status = TeacherProfile.Status.APPROVED
        profile.save()

    return redirect("registration_requests")


@login_required
def reject_registration(request, request_type, profile_id):

    if request.user.role != "admin":
        return redirect("home")

    if request.method != "POST":
        return redirect("registration_requests")

    if request_type == "student":

        profile = get_object_or_404(
            StudentProfile,
            id=profile_id
        )

        profile.status = StudentProfile.Status.REJECTED
        profile.save()

    elif request_type == "teacher":

        profile = get_object_or_404(
            TeacherProfile,
            id=profile_id
        )

        profile.status = TeacherProfile.Status.REJECTED
        profile.save()

    return redirect("registration_requests")
# ==========================================
# تعيين الطالب للمعلم
# ==========================================

@login_required
def assign_student_teacher(request, student_id):

    if request.user.role != "admin":
        return redirect("home")

    student = get_object_or_404(
        StudentProfile.objects.select_related("user", "teacher"),
        id=student_id
    )

    if request.method == "POST":

        form = AssignTeacherForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()

            return redirect(
                "student_detail",
                student_id=student.id
            )

    else:

        form = AssignTeacherForm(
            instance=student
        )

    return render(
        request,
        "dashboard/students/assign_teacher.html",
        {
            "student": student,
            "form": form,
        }
    )
