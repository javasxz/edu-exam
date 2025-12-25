from django.contrib.auth.models import BaseUserManager
from django.db.models import Q


class UserManager(BaseUserManager):
    # use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given phone number and password.
        """
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, login_field):
        return self.get(Q(email=login_field) | Q(phone_number=login_field))
