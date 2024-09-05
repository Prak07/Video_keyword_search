from django.db import models
from accounts.models import Profile
# Create your models here.
class Video(models.Model):
    username=models.CharField(max_length=100,null=True, blank=True)
    video=models.FileField(upload_to="video/%y")