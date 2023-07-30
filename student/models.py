from django.db import models
from redirector.models import AcademicYear,TestHistory,History
from home.models import *
from teacher.models import Teacher,Subject,cardType


class Student(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)
    profile_pic = models.ImageField(upload_to='student/profile/',null=True,blank=True)
    nationality = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    grade = models.CharField(max_length=255,null=True,blank=True)
    birth = models.DateField(null=True,blank=True)
    full_name = models.CharField(max_length=255,null=True,blank=True)
    instagram = models.CharField(max_length=5255,null=True,blank=True)
    telegram = models.CharField(max_length=5255,null=True,blank=True)
    view = models.BooleanField(default=True)
    year = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)
    is_verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,null=True)
    average = models.IntegerField(null=True,blank=True)
    new = models.BooleanField(default=False,null=True)
    def __str__(self):
        return self.username
    
class ResultHistory(models.Model):
    status = models.IntegerField()
    name = models.ForeignKey(TestHistory,on_delete=models.CASCADE)
    history = models.ForeignKey(History,on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subject,on_delete=models.CASCADE)
    time = models.CharField(max_length=255,null=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    year = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)


class Chat(models.Model):
    message = models.TextField(max_length=1000000,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    sender = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True)


class Library(models.Model):
    name = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='student/library',blank=True)
    file = models.FileField(upload_to='student/library')
    author = models.CharField(max_length=255,null=True,blank=True)
    disc = models.TextField(max_length=2555,null=True)
    for_student = models.BooleanField(default=True)
    posted_by = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    for_teacher = models.BooleanField(default=False)
    def __str__(self):
        return self.name



class Course(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to="student/course",blank=True)
    cover = models.ImageField(upload_to="student/course",blank=True)
    link = models.URLField(blank=True)
    posted_by = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    subject = models.ManyToManyField(Subject)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    about = models.TextField(max_length=5000)
    views = models.IntegerField(default=0)
    def __str__(self):
        return self.about


class CourseComment(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    message = models.TextField(max_length=5000,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    sender = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    
choice = (
    ("first academic term","first academic term"),
    ("second academic term","second academic term"),
)    

class Test(models.Model):
    name = models.CharField(max_length=255)
    grade = models.ManyToManyField(Grade)
    subject = models.ManyToManyField(Subject)
    time = models.CharField(choices=choice,max_length=255,null=True)
    year = models.ForeignKey(AcademicYear,null=True,on_delete=models.CASCADE)
    capacity = models.IntegerField()
    def __str__(self):
        return self.name
    

class Result(models.Model):
    status = models.IntegerField(null=True)
    name = models.ForeignKey(Test,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    year = models.ForeignKey(AcademicYear,null=True,on_delete=models.CASCADE)
    time = models.CharField(choices=choice,max_length=255,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)


class SubjectReslut(models.Model):
    first = models.IntegerField(null=True)
    f_from = models.IntegerField(null=True)
    s_from = models.IntegerField(null=True)
    second = models.IntegerField(null=True)
    year = models.FloatField(null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    time = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True)
    
    
class StudentStatus(models.Model):
    first_total = models.IntegerField(null=True)
    first_from = models.IntegerField(null=True)
    first_average = models.FloatField(null=True)
    second_total = models.IntegerField(null=True)
    second_from = models.IntegerField(null=True)
    second_average = models.FloatField(null=True)
    total = models.FloatField(null=True)
    average = models.FloatField(null=True)
    first_rank = models.IntegerField(null=True)
    second_rank = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    time = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)
    
    
    
    