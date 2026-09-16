import os
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Create or update the production admin user"

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "mohamedgad")
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            raise ValueError("ADMIN_PASSWORD environment variable is required")

        user, created = User.objects.get_or_create(username=username)

        user.role = User.Roles.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(f"Admin user {username} {action} successfully.")
        )
