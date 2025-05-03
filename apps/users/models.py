from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = None
    password = models.CharField(_("password"), max_length=200)
    terms_confirmed = models.BooleanField(default=False)
    full_name = models.CharField(_("full name"), max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email