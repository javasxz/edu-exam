from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create load test users"

    def handle(self, *args, **kwargs):
        PASSWORD = "testing321"
        TOTAL = 50

        for i in range(1, TOTAL + 1):
            email = f"user_{i}@example.com"
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    display_name=f"user_{i}",
                    email=email,
                    password=PASSWORD
                )

        self.stdout.write(self.style.SUCCESS("Users created successfully"))
