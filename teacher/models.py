from django.db import models
from home.models import *

class Subject(models.Model):
    name = models.CharField(max_length=255)
    grade = models.ManyToManyField(Grade)
    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    profile_pic = models.ImageField(upload_to='student/profile/',null=True,blank=True)
    my_room = models.ManyToManyField(Grade)
    nationality = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    instagram = models.CharField(max_length=5255,null=True,blank=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    telegram = models.CharField(max_length=5255,null=True,blank=True)
    facebook = models.URLField(null=True,blank=True)
    subject = models.ForeignKey(Subject,related_name="teacher_subjects",blank=True,on_delete=models.CASCADE,null=True)
    subscribers = models.ManyToManyField(Profile,related_name="teacher_Subscribers",blank=True)
    view = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    

class HomeRoom(models.Model):
    teacher = models.OneToOneField(Teacher,on_delete=models.CASCADE)
    room = models.OneToOneField(Grade,on_delete=models.CASCADE)
    year = models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.year
    

class GradePost(models.Model):
    for_grade = models.ForeignKey(Grade,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    disc = models.TextField(max_length=1000,null=True)
    link1 = models.URLField(blank=True)
    link2 = models.URLField(blank=True)
    link3 = models.URLField(blank=True)
    file1 = models.FileField(upload_to='teacher/posts',blank=True)
    file2 = models.FileField(upload_to='teacher/posts',blank=True)
    file3 = models.FileField(upload_to='teacher/posts',blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.title
    
    
class cardType(models.Model):
    name = models.CharField(max_length=255,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    table = models.BooleanField(default=True)
    st_name = models.BooleanField(default=True)
    st_grade = models.BooleanField(default=True)
    sc_icon = models.BooleanField(default=True)
    num = models.CharField(max_length=255,blank=True,null=True)
    select = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.name
    
    
class CTable(models.Model):
    cardTable = models.ForeignKey(cardType,on_delete=models.CASCADE)
    width = models.IntegerField(blank=True,null=True)
    height = models.IntegerField(blank=True,null=True)
    y_axis = models.IntegerField(blank=True,null=True)
    x_axis = models.IntegerField(blank=True,null=True)
    name_size = models.IntegerField(blank=True,null=True)
    name_font = models.CharField(max_length=2555,blank=True,null=True)
    num_size = models.IntegerField(blank=True,null=True)
    num_font = models.CharField(max_length=2555,blank=True,null=True)
    border = models.IntegerField(blank=True,null=True)
    
    
    
class StudentName(models.Model):
    cardTable = models.ForeignKey(cardType,on_delete=models.CASCADE)
    y_axis = models.IntegerField(blank=True,null=True)
    x_axis = models.IntegerField(blank=True,null=True)
    size = models.IntegerField(blank=True,null=True)
    font = models.CharField(max_length=2555,blank=True,null=True)
   
   
       
class StudentGrade(models.Model):
    cardTable = models.ForeignKey(cardType,on_delete=models.CASCADE)
    y_axis = models.IntegerField(blank=True,null=True)
    x_axis = models.IntegerField(blank=True,null=True)
    size = models.IntegerField(blank=True,null=True)
    font = models.CharField(max_length=2555,blank=True,null=True)
    
    
    
class icon(models.Model):
    cardTable = models.ForeignKey(cardType,on_delete=models.CASCADE)
    width = models.IntegerField(blank=True,null=True)
    height = models.IntegerField(blank=True,null=True)
    y_axis = models.IntegerField(blank=True,null=True)
    x_axis = models.IntegerField(blank=True,null=True)
    border = models.IntegerField(blank=True,null=True)
    
    
    
    
class Text(models.Model):
    cardTable = models.ForeignKey(cardType,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    text = models.TextField(max_length=5000,null=True)
    y_axis = models.IntegerField(blank=True,null=True)
    x_axis = models.IntegerField(blank=True,null=True)
    size = models.IntegerField(blank=True,null=True)
    font = models.CharField(max_length=2555,blank=True,null=True)
    def __str__(self):
        return self.name
 
 
 
class Line(models.Model):
    cardTable = models.ForeignKey(cardType,on_delete=models.CASCADE)
    name = models.IntegerField(null=True)
    y_axis = models.IntegerField(blank=True,null=True)
    x_axis = models.IntegerField(blank=True,null=True)
    width = models.IntegerField(blank=True,null=True)
    
    
