from common.models import BaseModel
from django.db import models

# Create your models here.
class Poll(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    expiry_date = models.DateTimeField()


class Choice(BaseModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)


class Thread(BaseModel):
    poll = models.OneToOneField(Poll, on_delete=models.CASCADE)


class Comment(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

