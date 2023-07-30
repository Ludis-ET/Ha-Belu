from django.db import models
from home.models import Profile,Grade


class Manager(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    profile_pic = models.ImageField(upload_to='student/profile/',null=True,blank=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    instagram = models.CharField(max_length=5255,null=True,blank=True)
    telegram = models.CharField(max_length=5255,null=True,blank=True)
    is_verified = models.BooleanField(default=False)


class StudentMessage(models.Model):
    image = models.ImageField(upload_to='manager/post',blank=True)
    title = models.CharField(max_length=255,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    message = models.TextField(max_length=1000,null=True)
    link_name = models.CharField(max_length=20,blank=True)
    link = models.CharField(max_length=2555,blank=True)
    sender = models.ForeignKey(Manager,on_delete=models.CASCADE,null=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.title
    