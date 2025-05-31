from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject


class Subscription(models.Model):
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.email
