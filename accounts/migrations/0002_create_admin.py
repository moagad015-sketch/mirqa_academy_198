import os

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_admin(apps, schema_editor):
    User = apps.get_model("accounts", "User")

    username = os.environ.get("ADMIN_USERNAME", "mohamedgad")
    password = os.environ.get("ADMIN_PASSWORD")

    if not password:
        return

    user, created = User.objects.get_or_create(username=username)

    user.password = make_password(password)
    user.role = "admin"
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()


def remove_admin(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    username = os.environ.get("ADMIN_USERNAME", "mohamedgad")
    User.objects.filter(username=username).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin, remove_admin),
    ]