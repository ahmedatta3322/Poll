from ast import Pass
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from common.models import BaseModel
from django.utils import timezone

# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    password = models.OneToOneField("user.Password", on_delete=models.CASCADE)

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


class Password(BaseModel):

    password = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)
    expired = models.BooleanField(default=False)

    def generate_password():
        """
        Generates a random password for this user
        """
        import random
        import string

        return "".join(random.choice(string.digits) for i in range(6))

    @property
    def is_expired(self):
        """
        Checks if the password has expired
        """
        return self.expires_at and self.expires_at < timezone.now()

    def __str__(self) -> str:
        return self.password
