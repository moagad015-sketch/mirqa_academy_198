from django import forms

from .models import (
    Course,
    Lesson,
    Announcement,
    Certificate,
    Exam,
    Question,
    Choice,
    ExamSection,
    ExamQuestion,
    SiteSettings,
    StudentProfile,
    TeacherProfile,
)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "description",
            "image",
            "is_active",
        ]


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            "title",
            "description",
            "video_url",
            "file",
            "order",
            "is_active",
        ]


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            "title",
            "content",
            "image",
            "is_active",
            "show_to_students",
            "show_to_teachers",
        ]


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = [
            "student",
            "course",
            "certificate_number",
            "student_name",
            "course_name",
            "grade",
            "is_valid",
        ]

        widgets = {
            "student_name": forms.TextInput(
                attrs={
                    "placeholder": "اسم الطالب في الشهادة"
                }
            ),
            "course_name": forms.TextInput(
                attrs={
                    "placeholder": "اسم الدورة في الشهادة"
                }
            ),
            "grade": forms.TextInput(
                attrs={
                    "placeholder": "التقدير"
                }
            ),
            "certificate_number": forms.TextInput(
                attrs={
                    "placeholder": "رقم الشهادة"
                }
            ),
        }


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam

        fields = [
            "course",
            "title",
            "description",
            "duration_minutes",
            "passing_score",
            "max_attempts",
            "status",
            "randomize_questions",
            "show_result_immediately",
            "start_at",
            "end_at",
        ]

        labels = {
            "course": "الدورة",
            "title": "اسم الاختبار",
            "description": "وصف الاختبار",
            "duration_minutes": "مدة الاختبار بالدقائق",
            "passing_score": "درجة النجاح",
            "max_attempts": "عدد المحاولات المسموح بها",
            "status": "حالة الاختبار",
            "randomize_questions": "ترتيب الأسئلة عشوائيًا",
            "show_result_immediately": "إظهار النتيجة مباشرة",
            "start_at": "موعد بداية الاختبار",
            "end_at": "موعد نهاية الاختبار",
        }

        widgets = {
            "course": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "اكتب اسم الاختبار"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "اكتب وصفًا مختصرًا للاختبار"
                }
            ),

            "duration_minutes": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثال: 30",
                    "min": "1"
                }
            ),

            "passing_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثال: 50",
                    "min": "0"
                }
            ),

            "max_attempts": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثال: 1",
                    "min": "1"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "randomize_questions": forms.CheckboxInput(
                attrs={
                    "class": "checkbox"
                }
            ),

            "show_result_immediately": forms.CheckboxInput(
                attrs={
                    "class": "checkbox"
                }
            ),

            "start_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                }
            ),

            "end_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["course"].empty_label = "اختر الدورة"

        self.fields["course"].queryset = Course.objects.filter(
            is_active=True
        ).order_by("title")


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question

        fields = [
            "course",
            "lesson",
            "text",
            "question_type",
            "difficulty",
            "points",
            "hint",
            "explanation",
            "is_active",
            "allow_random",
        ]

        labels = {
            "course": "الدورة",
            "lesson": "الدرس",
            "text": "نص السؤال",
            "question_type": "نوع السؤال",
            "difficulty": "درجة الصعوبة",
            "points": "درجة السؤال",
            "hint": "التلميح",
            "explanation": "شرح الإجابة",
            "is_active": "السؤال نشط",
            "allow_random": "السماح باستخدامه عشوائيًا",
        }

        widgets = {
            "course": forms.Select(
                attrs={"class": "form-control"}
            ),

            "lesson": forms.Select(
                attrs={"class": "form-control"}
            ),

            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "اكتب نص السؤال هنا..."
                }
            ),

            "question_type": forms.Select(
                attrs={"class": "form-control"}
            ),

            "difficulty": forms.Select(
                attrs={"class": "form-control"}
            ),

            "points": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1"
                }
            ),

            "hint": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "تلميح اختياري للطالب"
                }
            ),

            "explanation": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "شرح الإجابة بعد التصحيح"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={"class": "checkbox"}
            ),

            "allow_random": forms.CheckboxInput(
                attrs={"class": "checkbox"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["course"].empty_label = "اختر الدورة"
        self.fields["lesson"].empty_label = "اختر الدرس"

        self.fields["course"].queryset = Course.objects.filter(
            is_active=True
        ).order_by("title")

        self.fields["lesson"].queryset = Lesson.objects.filter(
            is_active=True
        ).order_by("order")


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice

        fields = [
            "text",
            "is_correct",
            "order",
        ]

        labels = {
            "text": "نص الاختيار",
            "is_correct": "الإجابة الصحيحة",
            "order": "ترتيب الاختيار",
        }

        widgets = {
            "text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "اكتب الاختيار"
                }
            ),

            "is_correct": forms.CheckboxInput(
                attrs={"class": "checkbox"}
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1"
                }
            ),
        }


class ExamSectionForm(forms.ModelForm):

    class Meta:
        model = ExamSection

        fields = [
            "title",
            "description",
            "order",
            "is_required",
        ]

        labels = {
            "title": "اسم القسم",
            "description": "وصف القسم",
            "order": "ترتيب القسم",
            "is_required": "القسم إجباري",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثال: القسم الأول — الاختيار من متعدد"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "وصف اختياري للقسم"
                }
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1"
                }
            ),

            "is_required": forms.CheckboxInput(
                attrs={"class": "checkbox"}
            ),
        }


class ExamQuestionForm(forms.ModelForm):

    class Meta:
        model = ExamQuestion

        fields = [
            "section",
            "question",
            "order",
            "points_override",
            "is_required",
        ]

        labels = {
            "section": "قسم الاختبار",
            "question": "السؤال",
            "order": "ترتيب السؤال",
            "points_override": "درجة السؤال داخل الاختبار",
            "is_required": "السؤال إجباري",
        }

        widgets = {
            "section": forms.Select(
                attrs={"class": "form-control"}
            ),

            "question": forms.Select(
                attrs={"class": "form-control"}
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1"
                }
            ),

            "points_override": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0"
                }
            ),

            "is_required": forms.CheckboxInput(
                attrs={"class": "checkbox"}
            ),
        }


class DirectExamQuestionForm(forms.Form):

    text = forms.CharField(
        label="نص السؤال",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "اكتب السؤال هنا..."
        })
    )

    question_type = forms.ChoiceField(
        label="نوع السؤال",
        choices=[
            ("mcq", "اختيار من متعدد"),
            ("true_false", "صح أو خطأ"),
            ("essay", "مقالي"),
        ],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    points = forms.IntegerField(
        label="درجة السؤال",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "1"
        })
    )

    section = forms.ModelChoiceField(
        label="قسم الاختبار",
        queryset=ExamSection.objects.none(),
        required=False,
        empty_label="بدون قسم",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    order = forms.IntegerField(
        label="ترتيب السؤال",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "1"
        })
    )

    choice_1 = forms.CharField(
        label="الاختيار الأول",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "الاختيار الأول"
        })
    )

    choice_2 = forms.CharField(
        label="الاختيار الثاني",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "الاختيار الثاني"
        })
    )

    choice_3 = forms.CharField(
        label="الاختيار الثالث",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "الاختيار الثالث"
        })
    )

    choice_4 = forms.CharField(
        label="الاختيار الرابع",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "الاختيار الرابع"
        })
    )

    correct_choice = forms.IntegerField(
        label="رقم الإجابة الصحيحة",
        required=False,
        min_value=1,
        max_value=4,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "1",
            "max": "4",
            "placeholder": "1 أو 2 أو 3 أو 4"
        })
    )

    def __init__(self, *args, exam=None, **kwargs):
        super().__init__(*args, **kwargs)

        if exam:
            self.fields["section"].queryset = exam.sections.all()

    def clean(self):
        cleaned_data = super().clean()

        question_type = cleaned_data.get("question_type")

        if question_type == "mcq":
            choices = [
                cleaned_data.get("choice_1"),
                cleaned_data.get("choice_2"),
                cleaned_data.get("choice_3"),
                cleaned_data.get("choice_4"),
            ]

            choices = [choice for choice in choices if choice]

            if len(choices) < 2:
                raise forms.ValidationError(
                    "يجب إضافة اختيارين على الأقل."
                )

            correct = cleaned_data.get("correct_choice")

            if not correct or correct > len(choices):
                raise forms.ValidationError(
                    "حدد رقم الإجابة الصحيحة بشكل صحيح."
                )

        elif question_type == "true_false":
            cleaned_data["choice_1"] = "صح"
            cleaned_data["choice_2"] = "خطأ"
            cleaned_data["correct_choice"] = (
                cleaned_data.get("correct_choice")
            )

            if cleaned_data["correct_choice"] not in [1, 2]:
                raise forms.ValidationError(
                    "في سؤال صح أو خطأ، اكتب 1 للصح أو 2 للخطأ."
                )

        return cleaned_data


# ==========================================
# فورم إعدادات الأكاديمية
# ==========================================

class SiteSettingsForm(forms.ModelForm):

    class Meta:
        model = SiteSettings

        fields = [
            "academy_name",
            "english_name",
            "slogan",
            "description",
            "logo",
            "email",
            "whatsapp_1",
            "whatsapp_2",
            "facebook_url",
            "instagram_url",
            "youtube_url",
            "is_active",
        ]

        labels = {
            "academy_name": "اسم الأكاديمية",
            "english_name": "الاسم بالإنجليزية",
            "slogan": "الشعار",
            "description": "وصف الأكاديمية",
            "logo": "شعار الأكاديمية",
            "email": "البريد الإلكتروني",
            "whatsapp_1": "رقم واتساب الأول",
            "whatsapp_2": "رقم واتساب الثاني",
            "facebook_url": "رابط فيسبوك",
            "instagram_url": "رابط إنستجرام",
            "youtube_url": "رابط يوتيوب",
            "is_active": "الأكاديمية مفعّلة",
        }

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 5
                }
            ),
        }


# ==========================================
# فورم تعيين الطالب للمعلم
# ==========================================

class AssignTeacherForm(forms.ModelForm):

    class Meta:
        model = StudentProfile

        fields = [
            "teacher",
        ]

        labels = {
            "teacher": "المعلم المسؤول عن الطالب",
        }

        widgets = {
            "teacher": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["teacher"].empty_label = "بدون معلم"

        self.fields["teacher"].queryset = (
            TeacherProfile.objects
            .filter(
                status=TeacherProfile.Status.APPROVED
            )
            .select_related("user")
            .order_by("user__username")
        )

        self.fields["teacher"].label_from_instance = (
            lambda teacher:
            f"{teacher.user.get_full_name() or teacher.user.username}"
        )