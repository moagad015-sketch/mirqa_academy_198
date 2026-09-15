from django.db import models
from django.conf import settings


# =========================
# ملفات الطلاب والمعلمين
# =========================

class StudentProfile(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "قيد المراجعة"
        APPROVED = "approved", "مقبول"
        REJECTED = "rejected", "مرفوض"
        SUSPENDED = "suspended", "موقوف"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    # المعلم المسؤول عن الطالب
    teacher = models.ForeignKey(
        "TeacherProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    # البيانات الأساسية
    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    # الدراسة والتخصص
    study_stage = models.CharField(
        max_length=200,
        blank=True
    )

    specialization = models.CharField(
        max_length=200,
        blank=True
    )

    current_level = models.CharField(
        max_length=200,
        blank=True
    )

    quran_memorization = models.CharField(
        max_length=300,
        blank=True
    )

    # المواعيد
    available_days = models.TextField(
        blank=True
    )

    available_times = models.TextField(
        blank=True
    )

    # مدة الحلقة المفضلة للطالب
    preferred_lesson_duration = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # حالة طلب التسجيل
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username


class TeacherProfile(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "قيد المراجعة"
        APPROVED = "approved", "مقبول"
        REJECTED = "rejected", "مرفوض"
        SUSPENDED = "suspended", "موقوف"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )

    # البيانات الأساسية
    phone = models.CharField(
        max_length=30,
        blank=True
    )

    # بيانات المعلم
    specializations = models.TextField(
        blank=True
    )

    qualification = models.CharField(
        max_length=300,
        blank=True
    )

    quran_memorization = models.CharField(
        max_length=300,
        blank=True
    )

    tajweed_level = models.CharField(
        max_length=300,
        blank=True
    )

    teaching_experience = models.TextField(
        blank=True
    )

    years_of_experience = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    ijazah = models.FileField(
        upload_to="teachers/ijazah/",
        null=True,
        blank=True
    )

    # المواعيد
    available_days = models.TextField(
        blank=True
    )

    available_times = models.TextField(
        blank=True
    )

    # نبذة عن المعلم
    bio = models.TextField(
        blank=True
    )

    # تسجيل التلاوة - أول وجه من سورة الطلاق
    recitation_audio = models.FileField(
        upload_to="teachers/recitations/",
        null=True,
        blank=True
    )

    # حالة طلب التسجيل
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username


# =========================
# الدورات
# =========================

class Course(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================
# الدروس والفيديوهات
# =========================

class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    video_url = models.URLField(
        blank=True
    )

    file = models.FileField(
        upload_to="lessons/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        default=1
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


# =========================
# تسجيل الطلاب في الدورات
# =========================

class Enrollment(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    progress = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return (
            f"{self.student.username} - "
            f"{self.course.title}"
        )


# =========================
# الشهادات
# =========================

class Certificate(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificates",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="certificates",
    )

    certificate_number = models.CharField(
        max_length=100,
        unique=True,
    )

    student_name = models.CharField(
        max_length=200,
        blank=True
    )

    course_name = models.CharField(
        max_length=200,
        blank=True
    )

    grade = models.CharField(
        max_length=100,
        blank=True
    )

    issued_at = models.DateTimeField(
        auto_now_add=True
    )

    is_valid = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.certificate_number


# =========================
# الإعلانات
# =========================

class Announcement(models.Model):

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    image = models.ImageField(
        upload_to="announcements/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    show_to_students = models.BooleanField(
        default=True
    )

    show_to_teachers = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# =========================
# إعدادات الأكاديمية
# =========================

class SiteSettings(models.Model):

    academy_name = models.CharField(
        max_length=200,
        default="أكاديمية مِرقاة"
    )

    english_name = models.CharField(
        max_length=200,
        default="Mirqā Academy"
    )

    slogan = models.CharField(
        max_length=300,
        default="نرتقي بالعلم، درجةً بعد درجة."
    )

    description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="settings/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True
    )

    whatsapp_1 = models.CharField(
        max_length=30,
        blank=True
    )

    whatsapp_2 = models.CharField(
        max_length=30,
        blank=True
    )

    facebook_url = models.URLField(
        blank=True
    )

    instagram_url = models.URLField(
        blank=True
    )

    youtube_url = models.URLField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.academy_name


# =========================
# نظام الاختبارات المتقدم
# =========================

class Exam(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "مسودة"
        PUBLISHED = "published", "منشور"
        OPEN = "open", "مفتوح"
        CLOSED = "مغلق"
        ARCHIVED = "archived", "مؤرشف"

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="exams",
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    passing_score = models.PositiveIntegerField(
        default=50
    )

    max_attempts = models.PositiveIntegerField(
        default=1
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    randomize_questions = models.BooleanField(
        default=False
    )

    show_result_immediately = models.BooleanField(
        default=True
    )

    start_at = models.DateTimeField(
        null=True,
        blank=True
    )

    end_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class ExamSection(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="sections"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    order = models.PositiveIntegerField(
        default=1
    )

    is_required = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.exam.title} - {self.title}"


class Question(models.Model):

    class QuestionType(models.TextChoices):
        MCQ = "mcq", "اختيار من متعدد"
        TRUE_FALSE = "true_false", "صح أو خطأ"
        ESSAY = "essay", "مقالي"
        AUDIO = "audio", "إجابة صوتية"

    class Difficulty(models.TextChoices):
        EASY = "easy", "سهل"
        MEDIUM = "medium", "متوسط"
        HARD = "hard", "صعب"

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="question_bank",
        null=True,
        blank=True
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        related_name="questions",
        null=True,
        blank=True
    )

    text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.MCQ
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM
    )

    points = models.PositiveIntegerField(
        default=1
    )

    hint = models.TextField(
        blank=True
    )

    explanation = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    allow_random = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.text[:80]


class Choice(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    text = models.CharField(
        max_length=500
    )

    is_correct = models.BooleanField(
        default=False
    )

    order = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text


class ExamQuestion(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="exam_questions"
    )

    section = models.ForeignKey(
        ExamSection,
        on_delete=models.SET_NULL,
        related_name="exam_questions",
        null=True,
        blank=True
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="exam_usages"
    )

    order = models.PositiveIntegerField(
        default=1
    )

    points_override = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    is_required = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "question"],
                name="unique_question_per_exam"
            )
        ]

    def get_points(self):
        if self.points_override is not None:
            return self.points_override
        return self.question.points

    def __str__(self):
        return f"{self.exam.title} - {self.question.text[:50]}"


class ExamAttempt(models.Model):

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "قيد الحل"
        SUBMITTED = "submitted", "تم التسليم"
        REVIEWING = "reviewing", "قيد التصحيح"
        GRADED = "graded", "تم التصحيح"

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_attempts"
    )

    attempt_number = models.PositiveIntegerField(
        default=1
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )

    passed = models.BooleanField(
        null=True,
        blank=True
    )

    teacher_feedback = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return (
            f"{self.student.username} - "
            f"{self.exam.title} - "
            f"محاولة {self.attempt_number}"
        )


class Answer(models.Model):

    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="answers"
    )

    text_answer = models.TextField(
        blank=True
    )

    audio_answer = models.FileField(
        upload_to="exam_answers/audio/",
        null=True,
        blank=True
    )

    awarded_points = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    is_correct = models.BooleanField(
        null=True,
        blank=True
    )

    is_manually_graded = models.BooleanField(
        default=False
    )

    teacher_feedback = models.TextField(
        blank=True
    )

    answered_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.attempt.student.username} - "
            f"{self.question.text[:50]}"
        )