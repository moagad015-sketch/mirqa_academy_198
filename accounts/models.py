from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "student", "طالب"
        TEACHER = "teacher", "معلم"
        ADMIN = "admin", "مدير"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )

    def __str__(self):
        return self.username