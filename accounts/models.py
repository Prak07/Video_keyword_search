from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    date_joined=models.DateTimeField(auto_now_add=True)
    last_updated=models.DateTimeField(auto_now=True)
    def __str__(self) :
        return self.username

class ForgotPass(models.Model):
    user=models.OneToOneField(Profile,on_delete=models.CASCADE)
    forgot_pass_token=models.CharField(max_length=100,blank=True,null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
