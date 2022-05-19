from common.models import BaseModel
from django.db import models
from django.utils import timezone

# Create your models here.
class Poll(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    expiry_date = models.DateTimeField()

    @property
    def is_expired(self):
        """
        Checks if the poll has expired
        """
        return self.expiry_date and self.expiry_date < timezone.now()


class UserCast(BaseModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey("poll.Choice", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)


class Choice(BaseModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)


class Thread(BaseModel):
    poll = models.OneToOneField(Poll, on_delete=models.CASCADE)


class Comment(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

