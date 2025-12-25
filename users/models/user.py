import uuid
import math

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.reverse import reverse

from common.models import TimeStambedModel
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    uid = models.CharField(unique=True, default=uuid.uuid1, max_length=50)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        error_messages={
            "unique": "This email address already exists. Please enter a new email address.",
        },
    )
    phone_number = PhoneNumberField(
        unique=True,
        blank=True,
        null=True,
        error_messages={
            "unique": "A user with the same mobile number already exists. Please enter a new mobile number.",
        },
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active."
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.get_username()

    def get_absolute_url(self):
        return reverse("users-detail", kwargs={"pk": self.pk})


class UserProfile(TimeStambedModel):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    GENDER_CHOICE = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (OTHER, _("Other")),
    )

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to="user/avatar/",
        validators=[FileExtensionValidator(["jpeg", "jpg", "png"])],
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICE, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return self.fullname()

    def fullname(self):
        return f"{self.first_name} {self.last_name}"
