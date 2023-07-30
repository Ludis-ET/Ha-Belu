from django.shortcuts import render,redirect
from .models import *
from student.models import Student
from teacher.models import Teacher
from manager.models import Manager
from staff.models import Staff
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import *
from django.views.decorators.clickjacking import xframe_options_exempt,xframe_options_sameorigin
from redirector.views import send_email
from redirector.models import AcademicYear
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from redirector.utils  import *
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags


@xframe_options_exempt
@xframe_options_sameorigin
def index(request):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    main_page = None
    main = None
    if Mainpage.objects.all().count() > 0:
        main = Mainpage.objects.all().first()
        main_page = Mainpage.objects.all().exclude(id=main.id)
    blog = Blog.objects.all()
    all = Mainpage.objects.all()
    type= " "
    context = {
        'web':web,
        'event':event,
        "main_page":main_page,
        'blog':blog,
        'type':type,
        'main':main,
        'all':all,
    }
    return render(request,'anonymous/index.html',context)


def login_page(request):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'],) 
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in Successfully')
                return redirect('r_index')
        else:
            messages.error(request,'Invalid user and password combination please try again')
    context = {
        'web':web,
        'event':event,
    }
    return render(request,'anonymous/login.html',context)


@xframe_options_exempt
@xframe_options_sameorigin
def about(request):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    about = About.objects.all()
    type= " "
    context = {
        'web':web,
        'event':event,
        'about':about,
        'type':type,
    }
    return render(request,'anonymous/about.html',context)


def teacher(request):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    type= " "
    teachers = Teacher.objects.filter(is_verified=True)
    context = {
        'web':web,
        'event':event,
        'type':type,
        'teachers':teachers,
    }
    return render(request,'anonymous/teachers.html',context)


def contact(request):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            Comment.objects.create(name=name,email=email,message=message)
            messages.success(request, "Hey '" + name + "' your comment is uploaded successfully Thank you! ")
            return redirect('a_contact')
        except:messages.error(request, "Error occured please Try Again")
    context = {
        'web':web,
        'event':event,
    }
    return render(request,'anonymous/contact.html',context)


def blog(request):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    blog = Blog.objects.all()
    category = Category.objects.all()
    context = {
        'web':web,
        'event':event,
        'blog':blog,
        'category':category,
    }
    return render(request,'anonymous/blog/blog.html',context)


def event(request,id):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    events = Event.objects.get(id=id)
    gallery = Gallery.objects.filter(event=id,on_front=True)
    category = Category.objects.all()
    context = {
        'web':web,
        'event':event,
        'category':category,
        'gallery':gallery,
        'events':events,
        'count':range(0,Gallery.objects.filter(event=id,on_front=True).count()+1),
    }
    return render(request,'anonymous/event.html',context)



def category(request,id):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    category = Category.objects.all()
    cat = Category.objects.get(id=id)
    blog = Blog.objects.filter(category=id)
    context = {
        'web':web,
        'event':event,
        'category':category,
        'blog':blog,
        'cat':cat,
    }
    return render(request,'anonymous/blog/category.html',context)


def blog_search(request):
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    blog = Blog.objects.all()
    category = Category.objects.all()
    if request.method == "POST":
        search = request.POST['search']
        searched = Blog.objects.filter(name__icontains=search)
        context = {
            'web':web,
            'event':event,
            'blog':blog,
            'category':category,
            'search':search,
            'searched':searched,
        }
        return render(request,'anonymous/blog/search.html',context)
    else:
        return redirect('a_blog')


def blog_post(request,id):
    man = request.user 
    web = Webpack.objects.get(id=1)
    event = Event.objects.all()
    blog = Blog.objects.get(id=id)
    blogs = Blog.objects.all()
    category = Category.objects.all()
    add = Addblog.objects.filter(blog=id)
    comment = Blog_comment.objects.filter(blog=id)
    if request.method=="POST":
        try:
            message = request.POST['message']
            Blog_comment.objects.create(message=message,commenter=man,blog=blog)
            messages.success(request, "Hey '" + man.first_name + "' your comment posted successfully!")
        except:messages.error(request, "Error occured please Try Again")
    context = {
        'web':web,
        'event':event,
        'blog':blog,
        'category':category,
        'add':add,
        'blogs':blogs,
        'comment':comment,
    }
    return render(request,'anonymous/blog/blog-post.html',context)



def register_user(request):
    web = Webpack.objects.get(id=1)
    if web.show_register == True:
        event = Event.objects.all()
        form = CreateUserForm()
        levels = Level.objects.all()
        grades = Grade.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name']
            username = request.POST['username']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            phone = request.POST['phone']
            sex = request.POST['sex']
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data["username"]  
                email=form.cleaned_data["email"]
                first_name=form.cleaned_data["first_name"]  
                last_name=form.cleaned_data["last_name"]
                password=form.cleaned_data["password1"]  
                user=User.objects.create_user(username, email, password)
                user.save()
                man = User.objects.get(username=username)
                man.first_name = first_name
                man.last_name = last_name
                man.save()
                user = User.objects.get(username=username)
                levell = request.POST['level']
                if levell:
                    level = Level.objects.get(name=levell)
                else:
                    level=None
                type = request.POST['type']
                if request.POST['type'] == 'student':
                    gradee = request.POST['grade']
                    grade = Grade.objects.get(name=gradee)
                    current_year = AcademicYear.objects.order_by('-id')[0]
                    Profile.objects.create(user=user,phone=phone,sex=sex,level=level,grade=grade,is_manager=False,is_teacher=False,is_student=True,is_staff=False)
                    pp = Profile.objects.get(user=user)
                    Password.objects.create(first_name=first_name, last_name=last_name,email=email,password=password1,phone=phone,sex=sex,level=level,grade=grade,type=type,of=man)
                    Student.objects.create(profile=pp,first_name=first_name,last_name=last_name,username=username,year=current_year,grade=grade.name)
                elif request.POST['type'] == 'teacher':
                    Profile.objects.create(user=user,phone=phone,sex=sex,level=level,is_manager=False,is_teacher=True,is_student=False,is_staff=False)
                    prof = Profile.objects.get(user=user)
                    Password.objects.create(first_name=first_name, last_name=last_name,email=email,password=password1,phone=phone,sex=sex,level=None,grade=None,type=type,of=man)
                    Teacher.objects.create(profile=prof,first_name=first_name,last_name=last_name)
                elif request.POST['type'] == 'manager':
                    Profile.objects.create(user=user,phone=phone,sex=sex,is_manager=True,is_teacher=False,is_student=False,is_staff=False)
                    prof = Profile.objects.get(user=user)
                    Password.objects.create(first_name=first_name, last_name=last_name,email=email,password=password1,phone=phone,sex=sex,level=None,grade=None,type=type,of=man)
                    Manager.objects.create(profile=prof,first_name=first_name,last_name=last_name)
                elif request.POST['type'] == 'staff':
                    Profile.objects.create(user=user,phone=phone,sex=sex,level=None,grade=None,is_manager=False,is_teacher=False,is_student=False,is_staff=True)
                    prof = Profile.objects.get(user=user)
                    Password.objects.create(first_name=first_name, last_name=last_name,email=email,password=password1,phone=phone,sex=sex,level=None,grade=None,type=type,of=man)
                    Staff.objects.create(profile=prof,first_name=first_name,last_name=last_name)
                else:pass
                send_email(user,request)
                messages.success(request, 'User Created successfully please login by your username and password')
                return redirect('login')
            else:
                messages.error(request, 'Username is in use or other userdata error please try again')
                return redirect('register')
        context = {
            'web':web,
            'event':event,
            'form':form,
            'levels':levels,
            'grades':grades,
        }
        return render(request,'anonymous/register.html',context)
    else:
        messages.error(request,'Registration is Closed for now!')
        return redirect('login')


@login_required(login_url='login')
def custom_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("r_index")

def reset_email(user,request):
    web = Webpack.objects.get(id=1)
    current_site = get_current_site(request)
    subject = "Reset your Password"
    body = render_to_string("anonymous/password-reset.html",{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
        'web':web
    })
    main = strip_tags(body)
    email = EmailMultiAlternatives(subject=subject,body=main,from_email=settings.EMAIL_HOST_USER,to=[user.email],)
    email.attach_alternative(body,'text/html')
    email.send()

def passReset(request):
    web = Webpack.objects.get(id=1)
    if request.method == 'POST':
        b = request.POST['username']
        if User.objects.filter(username=b):
            user = User.objects.get(username=b)
            reset_email(user,request)
            messages.success(request, "we've sent you a password reset email check it now in " + user.email)
        else:
            messages.error(request, "username not found.")
    context = {
        'web':web
    }
    return render(request,'anonymous/forget.html',context)


def forget_password(request,uidb64,token):
    uid=force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if account_activation_token.check_token(user,token):
        web = Webpack.objects.get(pk=1)
        if request.method == 'POST':
            a = request.POST['password1']
            user.set_password(a)
            p = Password.objects.get(of=user.id)
            p.password = a
            p.save()
            user.save()
            messages.success(request, "password changed succesfully!")
            return redirect('login')
        context = {
            'web':web,
        }
        return render(request,'anonymous/new-password.html',context)


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request,):
    return render(request, '500.html', status=500)


def handler302(request,):
    return render(request, '500.html', status=302)


def handler400(request, exception):
    return render(request, '403.html', status=400)

def handler403(request, exception):
    return render(request, '403.html', status=403)