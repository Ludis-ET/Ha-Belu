from django.db import models
from django.contrib.auth.models import User

class Level(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Grade(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey(Level,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    



class Mainpage(models.Model):
    image = models.ImageField(upload_to="anonymous/webpack/",null=True,blank=True)
    header = models.CharField(max_length=255,null=True,blank=True)
    body = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.header
    


# Create your models here.
class Webpack(models.Model):
    full_name = models.CharField(max_length=255,blank=True, null=True)
    icon = models.ImageField(upload_to="anonymous/webpack/",blank=True, null=True)
    slogan = models.CharField(max_length=500,blank=True,null=True)
    about = models.TextField(max_length=1000,blank=True,null=True)
    app = models.FileField(upload_to="anonymous/webpack/",blank=True,null=True)
    theme_color = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    show_register = models.BooleanField(null=True,default=False,blank=False)
    registration_deadline = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    phone1 = models.CharField(max_length=255, blank=True, null=True)
    phone2 = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.full_name
    


class Event(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.name

class Gallery(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to="anonymous/gallery/",null=True)
    on_front = models.BooleanField(default=False,null=True)

    
class Category(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.name


class Password(models.Model):
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=255,null=True)
    sex = models.CharField(max_length=255,null=True)
    level = models.CharField(max_length=255,null=True)
    grade = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=255,null=True)
    of = models.OneToOneField(User,on_delete=models.CASCADE,null=True,related_name="user_password")
    def __str__(self):
        return self.first_name
    


class Blog(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    cover = models.ImageField(upload_to="anonymous/blog/",blank=True,null=True)
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    p1 = models.TextField(max_length=5000,null=True,blank=True)
    p2 = models.TextField(max_length=5000,null=True,blank=True)
    p3 = models.TextField(max_length=5000,null=True,blank=True)
    by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name


class Addblog(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    Image = models.ImageField(upload_to="anonymous/blog/",blank=True,null=True)
    blog = models.ForeignKey(Blog,null=True,blank=True,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    p1 = models.TextField(max_length=5000,null=True,blank=True)
    p2 = models.TextField(max_length=5000,null=True,blank=True)
    p3 = models.TextField(max_length=5000,null=True,blank=True)
    def __str__(self):
        return self.name
    

class About(models.Model):
    topic = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to="anonymous/about/",null=True,blank=True)
    paragraph = models.TextField(max_length=2555,null=True,blank=True)
    def __str__(self):
        return self.topic


class Comment(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField()
    message = models.TextField(max_length=2555,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.name
    
    
class Blog_comment(models.Model):
    commenter = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    message = models.TextField(max_length=2555,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    phone = models.CharField(max_length=255,null=True)
    sex = models.CharField(max_length=255,null=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=True,blank=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,null=True,blank=True)
    is_manager = models.BooleanField(default=False,null=True)
    is_teacher = models.BooleanField(default=False,null=True)
    is_student = models.BooleanField(default=True,null=True)
    is_staff = models.BooleanField(default=False,null=True)
    is_verified = models.BooleanField(default=False,null=True)
    def __str__(self):
        return self.phone
    