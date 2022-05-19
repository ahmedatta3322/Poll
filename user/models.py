from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = "email"
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    @property
    def is_expired(self):
        """
        Checks if the password has expired
        """
        print(self.created_at, timezone.now())
        return self.created_at + timedelta(minutes=10) < timezone.now()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def expire_password(self):
        """
        Expires the password for this user
        """
        self.password = self.generate_password()
        self.save()

    def generate_password():
        """
        Generates a random password for this user
        """
        import random
        import string

        return "".join(random.choice(string.digits) for i in range(6))

