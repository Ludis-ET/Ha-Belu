from django.db import models
from home.models import Profile,Grade


class Staff(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    profile_pic = models.ImageField(upload_to='staff/profile/',null=True,blank=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    report_card = models.BooleanField(default=True)
    verify_user = models.BooleanField(default=True)
    modify_student = models.BooleanField(default=True)
    transfer = models.BooleanField(default=False)
    time = models.BooleanField(default=False)
    data = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name
    