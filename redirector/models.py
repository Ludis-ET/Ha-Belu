from django.db import models
from django.contrib.auth.models import User
from teacher.models import Subject

class AcademicYear(models.Model):
    year = models.IntegerField(null=True)
    new = models.BooleanField(default=False,null=True)
    start = models.BooleanField(default=False,null=True)
    


class History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    academicYear = models.ForeignKey(AcademicYear,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)
    nationality = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True)
    sex = models.CharField(max_length=255,null=True)
    level = models.CharField(max_length=255,null=True)
    grade = models.CharField(max_length=255,null=True)
    is_manager = models.BooleanField(default=False,null=True)
    is_teacher = models.BooleanField(default=False,null=True)
    is_student = models.BooleanField(default=True,null=True)
    is_staff = models.BooleanField(default=False,null=True)
    is_verified = models.BooleanField(default=False,null=True)
    birth = models.DateField(null=True,blank=True)
    instagram = models.CharField(max_length=5255,null=True,blank=True)
    telegram = models.CharField(max_length=5255,null=True,blank=True)
    def __str__(self):
        return self.first_name


class TestHistory(models.Model):
    name = models.CharField(max_length=255)
    history = models.ForeignKey(History,on_delete=models.CASCADE)
    capacity = models.IntegerField()
    academicYear = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)
    time = models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.name
    

class SubjectReslutHistory(models.Model):
    first = models.IntegerField(null=True)
    f_from = models.IntegerField(null=True)
    s_from = models.IntegerField(null=True)
    second = models.IntegerField(null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    student = models.ForeignKey(History,on_delete=models.CASCADE)
    time = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)
    
    
class StudentStatusHistory(models.Model):
    first_total = models.IntegerField(null=True)
    first_from = models.IntegerField(null=True)
    first_average = models.FloatField(null=True)
    second_total = models.IntegerField(null=True)
    second_from = models.IntegerField(null=True)
    second_average = models.FloatField(null=True)
    average = models.FloatField(null=True)
    first_rank = models.IntegerField(null=True)
    second_rank = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    student = models.ForeignKey(History,on_delete=models.CASCADE)
    time = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)