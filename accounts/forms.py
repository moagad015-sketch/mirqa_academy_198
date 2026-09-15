from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from academy.models import StudentProfile, TeacherProfile


# =========================
# نموذج تسجيل الطالب
# =========================

class StudentRegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="البريد الإلكتروني"
    )

    phone = forms.CharField(
        required=True,
        label="رقم الهاتف"
    )

    age = forms.IntegerField(
        required=True,
        min_value=1,
        label="العمر"
    )

    study_stage = forms.CharField(
        required=True,
        label="المرحلة الدراسية"
    )

    specialization = forms.CharField(
        required=True,
        label="التخصص المطلوب"
    )

    current_level = forms.CharField(
        required=False,
        label="المستوى الحالي"
    )

    quran_memorization = forms.CharField(
        required=False,
        label="مقدار حفظ القرآن"
    )

    available_days = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="الأيام المتاحة"
    )

    available_times = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="المواعيد المتاحة"
    )

    preferred_lesson_duration = forms.IntegerField(
        required=False,
        min_value=15,
        label="مدة الحلقة المفضلة بالدقائق"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

        labels = {
            "username": "اسم المستخدم",
        }

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "اسم المستخدم مستخدم بالفعل، اختر اسمًا آخر."
            )

        return username

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = User.Roles.STUDENT

        if commit:
            user.save()

            StudentProfile.objects.create(
                user=user,
                age=self.cleaned_data["age"],
                phone=self.cleaned_data["phone"],
                study_stage=self.cleaned_data["study_stage"],
                specialization=self.cleaned_data["specialization"],
                current_level=self.cleaned_data["current_level"],
                quran_memorization=self.cleaned_data[
                    "quran_memorization"
                ],
                available_days=self.cleaned_data[
                    "available_days"
                ],
                available_times=self.cleaned_data[
                    "available_times"
                ],
                preferred_lesson_duration=self.cleaned_data[
                    "preferred_lesson_duration"
                ],
            )

        return user


# =========================
# نموذج تسجيل المعلم
# =========================

class TeacherRegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="البريد الإلكتروني"
    )

    phone = forms.CharField(
        required=True,
        label="رقم الهاتف"
    )

    specializations = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="التخصصات التي يستطيع تدريسها"
    )

    qualification = forms.CharField(
        required=True,
        label="المؤهل الدراسي"
    )

    quran_memorization = forms.CharField(
        required=True,
        label="مقدار حفظ القرآن"
    )

    tajweed_level = forms.CharField(
        required=True,
        label="مستوى التجويد النظري والعملي"
    )

    teaching_experience = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="الخبرة في تعليم القرآن"
    )

    years_of_experience = forms.IntegerField(
        required=True,
        min_value=0,
        label="سنوات الخبرة"
    )

    ijazah = forms.FileField(
        required=False,
        label="الإجازة إن وجدت"
    )

    available_days = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="الأيام المتاحة"
    )

    available_times = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="المواعيد المتاحة"
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="نبذة عن المعلم"
    )

    recitation_audio = forms.FileField(
        required=True,
        label="تسجيل تلاوة أول وجه من سورة الطلاق"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

        labels = {
            "username": "اسم المستخدم",
        }

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "اسم المستخدم مستخدم بالفعل، اختر اسمًا آخر."
            )

        return username

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = User.Roles.TEACHER

        if commit:
            user.save()

            TeacherProfile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                specializations=self.cleaned_data[
                    "specializations"
                ],
                qualification=self.cleaned_data[
                    "qualification"
                ],
                quran_memorization=self.cleaned_data[
                    "quran_memorization"
                ],
                tajweed_level=self.cleaned_data[
                    "tajweed_level"
                ],
                teaching_experience=self.cleaned_data[
                    "teaching_experience"
                ],
                years_of_experience=self.cleaned_data[
                    "years_of_experience"
                ],
                ijazah=self.cleaned_data["ijazah"],
                available_days=self.cleaned_data[
                    "available_days"
                ],
                available_times=self.cleaned_data[
                    "available_times"
                ],
                bio=self.cleaned_data["bio"],
                recitation_audio=self.cleaned_data[
                    "recitation_audio"
                ],
            )

        return user