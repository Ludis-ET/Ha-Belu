from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from home.models import *
from django.contrib.sites.shortcuts import get_current_site
from home.forms import *
from .models import *
from redirector.models import *
import datetime
from teacher.models import Teacher,Subject,HomeRoom
from student.models import *
from django.contrib import messages
from django.db.models import Sum
from staff.models import Staff



@login_required(login_url='login')
def index(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    managers = Manager.objects.all()
    users = User.objects.all()
    male = Profile.objects.filter(sex="male").count()
    female = Profile.objects.filter(sex="female").count()
    m_per = (male/users.count())*100
    f_per = (female/users.count())*100
    st_per = (students.count()/users.count())*100
    te_per = (teachers.count()/users.count())*100
    ma_per = (managers.count()/users.count())*100
    this_month = datetime.datetime.now().month
    month = User.objects.filter(date_joined__month=this_month)
    mmm = StudentMessage.objects.all().count()
    c = Comment.objects.all()
    y = AcademicYear.objects.last().year
    if mmm>2:
        sm = StudentMessage.objects.filter(sender=manager)[(mmm-2):mmm]
    else:
        sm = StudentMessage.objects.filter(sender=manager)[:mmm]
    if request.method == 'POST':
        if 'send' in request.POST:
            a = request.POST['message']
            StudentMessage.objects.create(message=a,title="MR. "+manager.first_name+" "+manager.last_name,sender=manager)
            messages.success(request,"Message sent!")
            return redirect('r_index')
        if 'delete' in request.POST:
            id = request.POST['id']
            d = Comment.objects.get(id=id)
            d.delete()
            messages.success(request,'Feedback deleted')
            return redirect('r_index')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'students':students,
        'managers':managers,
        'users':users,
        'st_per':st_per,
        'te_per':te_per,
        'ma_per':ma_per,
        'teachers':teachers,
        'm_per':m_per,
        'f_per':f_per,
        'male':male,
        'female':female,
        'c':c,
        'month':month,
        'sm':sm,
        'last_year':y,
    }
    return render(request,'manager/index.html',context)


@login_required(login_url='login')
def table(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    managers = Manager.objects.all()
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'last_year':y,
        'user':user,
        'manager':manager,
        'students':students,
        'managers':managers,
        'teachers':teachers,
    }
    return render(request,'manager/user/user tabel.html',context)


@login_required(login_url='login')
def studenttable(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    students = Student.objects.all()
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'last_year':y,
        'user':user,
        'manager':manager,
        'students':students,
    }
    return render(request,'manager/user/student tabel.html',context)


@login_required(login_url='login')
def studenttable(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    students = Student.objects.all()
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'user':user,
        'last_year':y,
        'manager':manager,
        'students':students,
    }
    return render(request,'manager/user/student tabel.html',context)


@login_required(login_url='login')
def accepttable(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    managers = Manager.objects.all()
    staffs = Staff.objects.all()
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'students':students,
        'last_year':y,
        'managers':managers,
        'teachers':teachers,'staffs':staffs,
    }
    return render(request,'manager/user/accept tabel.html',context)


@login_required(login_url='login')
def managertable(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    students = Manager.objects.all()
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'students':students,
        'last_year':y,
    }
    return render(request,'manager/user/manager tabel.html',context)


@login_required(login_url='login')
def manageradd(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    y = AcademicYear.objects.last().year
    grade = Grade.objects.all()
    if request.method == 'POST':
        a = request.POST['first_name']
        b = request.POST['last_name']
        h = request.POST['username']
        c = request.POST['email']
        d = request.POST['password1']
        e = request.POST['password2']
        f = request.POST['sex']
        g = request.POST['phone']
        if d != e:
            messages.error(request,"passwords doesnot match")
        elif User.objects.filter(username=h).exists():
            messages.error(request,"username is in use please change it")
        else:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data["username"]  
                email=form.cleaned_data["email"]
                first_name=form.cleaned_data["first_name"]  
                last_name=form.cleaned_data["last_name"]
                password=form.cleaned_data["password1"]  
                year = AcademicYear.objects.last()
                user=User.objects.create_user(username, email, password)
                user.first_name = a
                user.last_name = b
                user.save()
                Password.objects.create(of=user,first_name=first_name,last_name=last_name,password=d)
                profile = Profile.objects.create(is_verified=True,user=user,phone=g,sex=f,grade=None,level=None,is_teacher=False,is_manager=True,is_staff=False,is_student=False)
                profile.save()
                student = Manager.objects.create(profile=profile,first_name=first_name,last_name=last_name,is_verified=True)
                student.save()
                messages.success(request,'Manager added Successfully!')
            else:
                messages.error(request,'password type error it must me greator than 8 and it have to have a capital letters.....')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        #'student':students,
        'grade':grade,
        'last_year':y,
    }
    return render(request,'manager/user/manager add.html',context)


@login_required(login_url='login')
def teachertable(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    students = Teacher.objects.all()
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        'students':students,
    }
    return render(request,'manager/user/teacher tabel.html',context)


@login_required(login_url='login')
def studentedit(request,username):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    u = User.objects.get(username=username)
    p = Profile.objects.get(user=u)
    students = Student.objects.get(username=username)
    grade = Grade.objects.all().exclude(name=students.grade)
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        select = request.POST['select']
        sub = Grade.objects.get(id=select)
        students.grade=sub.name
        p.grade=sub
        p.save()
        students.save()
        messages.success(request,'Updated Successfully!')
        return redirect('m_student_edit',username)
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'student':students,
        'last_year':y,
        'grade':grade,
    }
    return render(request,'manager/user/student edit.html',context)


@login_required(login_url='login')
def studentadd(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    grade = Grade.objects.all()
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        select = request.POST['select']
        sub = Grade.objects.get(id=select)
        a = request.POST['first_name']
        b = request.POST['last_name']
        h = request.POST['username']
        c = request.POST['email']
        d = request.POST['password1']
        e = request.POST['password2']
        f = request.POST['sex']
        g = request.POST['phone']
        if d != e:
            messages.error(request,"passwords doesnot match")
        elif User.objects.filter(username=h).exists():
            messages.error(request,"username is in use please change it")
        else:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data["username"]  
                email=form.cleaned_data["email"]
                first_name=form.cleaned_data["first_name"]  
                last_name=form.cleaned_data["last_name"]
                password=form.cleaned_data["password1"]  
                year = AcademicYear.objects.last()
                user=User.objects.create_user(username, email, password)
                user.first_name = a
                user.last_name = b
                user.save()
                Password.objects.create(of=user,first_name=first_name,last_name=last_name,password=d)
                profile = Profile.objects.create(is_verified=True,user=user,phone=g,sex=f,grade=sub,level=None,is_teacher=False,is_manager=False,is_staff=False,is_student=True)
                profile.save()
                student = Student.objects.create(year=year,profile=profile,first_name=first_name,last_name=last_name,username=username,is_verified=True,grade=sub.name)
                student.save()
                messages.success(request,'Student added Successfully!')
            else:
                messages.error(request,'password type error it must me greator than 8 and it have to have a capital letters.....')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        #'student':students,
        'grade':grade,
    }
    return render(request,'manager/user/student add.html',context)

@login_required(login_url='login')
def staffadd(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    grade = Grade.objects.all()
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        a = request.POST['first_name']
        b = request.POST['last_name']
        h = request.POST['username']
        c = request.POST['email']
        d = request.POST['password1']
        e = request.POST['password2']
        g = request.POST['phone']
        if d != e:
            messages.error(request,"passwords doesnot match")
        elif User.objects.filter(username=h).exists():
            messages.error(request,"username is in use please change it")
        else:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data["username"]  
                email=form.cleaned_data["email"]
                first_name=form.cleaned_data["first_name"]  
                last_name=form.cleaned_data["last_name"]
                password=form.cleaned_data["password1"]  
                year = AcademicYear.objects.last()
                user=User.objects.create_user(username, email, password)
                user.first_name = a
                user.last_name = b
                user.save()
                Password.objects.create(of=user,first_name=first_name,last_name=last_name,password=d)
                profile = Profile.objects.create(is_verified=True,user=user,phone=g,sex=None,grade=None,level=None,is_teacher=False,is_manager=False,is_staff=True,is_student=False)
                profile.save()
                staff = Staff.objects.create(profile=profile,first_name=first_name,last_name=last_name,is_verified=True)
                staff.save()
                messages.success(request,'Staff added Successfully!')
            else:
                messages.error(request,'password type error it must me greator than 8 and it have to have a capital letters.....')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        #'student':students,
        'grade':grade,
    }
    return render(request,'manager/staff/add.html',context)


@login_required(login_url='login')
def staffedit(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    grade = Grade.objects.all()
    y = AcademicYear.objects.last().year
    staffes = Staff.objects.filter(is_verified=True)
    if request.method == 'POST':
        user = request.POST['user']
        s = Staff.objects.get(id=user)
        a = request.POST.get('a')
        b = request.POST.get('b')
        c = request.POST.get('c')
        d = request.POST.get('d')
        e = request.POST.get('e')
        f = request.POST.get('f')
        if a == 'on':
            s.report_card = True
        else:
            s.report_card = False
        if b == 'on':
            s.verify_user = True
        else:
            s.verify_user = False
        if c == 'on':
            s.modify_student = True
        else:
            s.modify_student = False
        if d == 'on':
            s.transfer = True
        else:
            s.transfer = False
        if e == 'on':
            s.time = True
        else:
            s.time = False
        if f == 'on':
            s.data = True
        else:
            s.data = False
        s.save()
        messages.success(request,'succesfully updated')
            
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        'staffes':staffes,
        #'student':students,
        'grade':grade,
    }
    return render(request,'manager/staff/edit.html',context)




@login_required(login_url='login')
def teacheredit(request,username):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    u = User.objects.get(username=username)
    p = Profile.objects.get(user=u)
    students = Teacher.objects.get(profile=p)
    grade = Subject.objects.all().exclude(name=students.subject)
    g = Grade.objects.all().exclude(id__in=students.my_room.all())
    y = AcademicYear.objects.last().year
    select=None
    if request.method == 'POST':
        select = request.POST.getlist('select')
        students.my_room.set(select)
        students.save()
        sub = request.POST['subject']
        subj = Subject.objects.get(id=sub)
        students.subject=subj
        students.save()
        messages.success(request,'Updated Successfully!')
        return redirect('m_teacher_edit',username)
    context = {
        "web":web,
        'last_year':y,
        'user':user,
        'manager':manager,
        'g':g,
        'student':students,
        'grade':grade,
        'select':select
    }
    return render(request,'manager/user/teacher edit.html',context)


@login_required(login_url='login')
def teacheradd(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    grade = Subject.objects.all()
    g = Grade.objects.all()
    y = AcademicYear.objects.last().year
    select=None
    if request.method == 'POST':
        select = request.POST.getlist('select')
        sub = request.POST['subject']
        subj = Subject.objects.get(id=sub)
        a = request.POST['first_name']
        b = request.POST['last_name']
        h = request.POST['username']
        c = request.POST['email']
        d = request.POST['password1']
        e = request.POST['password2']
        f = request.POST['sex']
        g = request.POST['phone']
        if d != e:
            messages.error(request,"passwords doesnot match")
        elif User.objects.filter(username=h).exists():
            messages.error(request,"username is in use please change it")
        else:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data["username"]  
                email=form.cleaned_data["email"]
                first_name=form.cleaned_data["first_name"]  
                last_name=form.cleaned_data["last_name"]
                password=form.cleaned_data["password1"]  
                year = AcademicYear.objects.last()
                user=User.objects.create_user(username, email, password)
                user.first_name = a
                user.last_name = b
                user.save()
                Password.objects.create(of=user,first_name=first_name,last_name=last_name,password=d)
                profile = Profile.objects.create(is_verified=True,user=user,phone=g,sex=f,grade=None,level=None,is_teacher=True,is_manager=False,is_staff=False,is_student=False)
                profile.save()
                teacher = Teacher.objects.create(profile=profile,nationality='Ethiopian',first_name=a,last_name=b,subject=subj,is_verified=True)
                teacher.my_room.set(select)
                teacher.save()
                messages.success(request,'Teacher Added Successfully!')
                return redirect('m_teacher_add')
            else:
                messages.error(request,'password type error it must me greator than 8 and it have to have a capital letters.....')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'g':g,
        'grade':grade,
        'last_year':y,
        'select':select
    }
    return render(request,'manager/user/teacher add.html',context)


@login_required(login_url='login')
def deleteuser(request):
    if request.method == 'POST':
        a = request.POST['username']
        u = User.objects.get(username=a)
        u.delete()
        messages.success(request,"User deleted!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
@login_required(login_url='login')
def acceptuser(request):
    if request.method == 'POST':
        b = request.POST['username']
        a = request.POST['type']
        u = User.objects.get(username=b)
        p = Profile.objects.get(user=u)
        if a == 's':
            s = Student.objects.get(profile=p)
        elif a == 't':
            s = Teacher.objects.get(profile=p)
        elif a == 'm':
            s = Manager.objects.get(profile=p)
        elif a == 'ss':
            s = Staff.objects.get(profile=p)
        else:
            messages.error(request,"Unknown User Type")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if 'accept' in request.POST:
            s.is_verified=True
            s.save()
            messages.success(request,"User accepted to this website!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'deny' in request.POST:
            s.is_verified=False
            s.save()
            messages.success(request,"User rejected from this website!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required(login_url='login')
def displayweb(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    current_site = get_current_site(request)
    w = Mainpage.objects.all()
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        if 'one' in request.POST:
            a = request.POST['name']
            b = request.POST['slogan']
            c = request.POST['about']
            if request.FILES:
                d = request.FILES['icon']
                web.icon=d
                web.full_name = a
                web.about=c
                web.slogan=b
                web.save()
                messages.success(request,"Website informaiton chaned you can see the result in the preview")
                return redirect('m_web_display')
            else:
                web.full_name = a
                web.about=c
                web.slogan=b
                web.save()
                messages.success(request,"Website informaiton chaned you can see the result in the preview")
                return redirect('m_web_display')
        if 'two' in request.POST:
            if request.FILES:
                a = request.FILES['image']
                b = request.POST['head']
                c = request.POST['body']
                Mainpage.objects.create(image=a,header=b,body=c)
                messages.success(request,"Wow new home design inserted see the change")
                return redirect('m_web_display')
        if 'three' in request.POST:
            a = request.POST['color']
            web.theme_color=a
            web.save()
            messages.success(request,"Wow new theme color detected see the change")
            return redirect('m_web_display')
        if 'four' in request.POST:
            a = request.POST['address']
            b = request.POST['email']
            c = request.POST['phone1']
            d = request.POST['phone2']
            e = request.POST['telegram']
            f = request.POST['facebook']
            web.address=a
            web.email=b
            web.phone1=c
            web.phone2=d
            web.telegram=e
            web.facebook=f
            web.save()
            messages.success(request,"Additional Information added succesfully!")
            return redirect('m_web_display')
        if 'five' in request.POST:
            a = request.POST['id']
            w = Mainpage.objects.get(id=a)
            w.delete()
            messages.success(request,"selected home content deleted")
            return redirect('m_web_display')
        if 'six' in request.POST:
            a = request.POST['date']
            b = request.POST.get('show')
            if a:
                web.registration_deadline=a
            if b:
                web.show_register=True
            if not b:
                web.show_register=False
            web.save()
            messages.success(request,"Alter in registration date detected")
            return redirect('m_web_display')
    context = {
        "web":web,
        'user':user,
        'last_year':y,
        'manager':manager,
        'site':current_site,
        'w':w,
    }
    return render(request,'manager/web/display.html',context)

 
@login_required(login_url='login')
def displayabout(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    abouts = About.objects.all()
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        if 'one' in request.POST:
            b = request.POST['title']
            c = request.POST['detail']
            if request.FILES:
                a = request.FILES['image']
                About.objects.create(image=a,topic=b,paragraph=c)
                messages.success(request,'Posted Successfully')
                return redirect('m_web_about')
            else:
                About.objects.create(topic=b,paragraph=c)
                messages.success(request,'Posted Successfully')
                return redirect('m_web_about')
        if 'update' in request.POST:
            b = request.POST['title']
            c = request.POST['detail']
            d = request.POST['id']
            aaa = About.objects.get(pk=d)
            if request.FILES:
                a = request.FILES['image']
                aaa.topic=b
                aaa.Image=a
                aaa.paragraph=c
                aaa.save()
                messages.success(request,'Posted updated')
            else:
                aaa.topic=b
                aaa.paragraph=c
                aaa.save()
                messages.success(request,'Posted updated')
        if 'delete' in request.POST:
            b = request.POST['title']
            c = request.POST['detail']
            d = request.POST['id']
            aaa = About.objects.get(pk=d)
            aaa.delete()
            messages.success(request,'Posted deleted')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        'abbs':abouts,
    }
    return render(request,'manager/web/about.html',context)


@login_required(login_url='login')
def blog(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    b = Blog.objects.filter(by=user)
    ab = Addblog.objects.all()
    y = AcademicYear.objects.last().year
    c = Category.objects.all()
    if request.method == 'POST':
        a = request.POST['name']
        if not a:
            messages.error(request,'We canot detect any change please add something')
        elif Category.objects.filter(name=a).exists():
            messages.error(request,'Category name existed please change new name')
        else:
            Category.objects.create(name=a)
            messages.success(request,"New Category Added")
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'b':b,
        'ab':ab,
        'last_year':y,
        'ca':c,
    }
    return render(request,'manager/blog/blog.html',context)


@login_required(login_url='login')
def addblog(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    y = AcademicYear.objects.last().year
    b = Category.objects.all()
    if request.method == 'POST':
        if request.FILES:
            a = request.POST['name']
            b = request.FILES['cover']
            c = request.POST['category']
            cc = Category.objects.get(pk=c)
            d = request.POST.get('p1')
            e = request.POST.get('p2')
            f = request.POST.get('p3')
            aa = Blog.objects.create(name=a,cover=b,category=cc,by=user)
            if d:
                aa.p1=d
            if e:
                aa.p2=e
            if f:
                aa.p3=f
            aa.save()
            messages.success(request,'New blogpost added successfuly')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        'b':b,
    }
    return render(request,'manager/blog/add blog.html',context)


@login_required(login_url='login')
def editmainblog(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    bb = Blog.objects.get(pk=id)
    b = Category.objects.all().exclude(name=bb.category.name)
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
            a = request.POST['name']
            c = request.POST['category']
            cc = Category.objects.get(pk=c)
            d = request.POST.get('p1')
            e = request.POST.get('p2')
            f = request.POST.get('p3')
            if request.FILES:
                b = request.FILES['cover']
                bb.cover=b
                bb.save()
            if d:
                bb.p1=d
                bb.save()
            if e:
                bb.p2=e
                bb.save()
            if f:
                bb.p3=f
                bb.save()
            if c:
                bb.category=cc
                bb.save()
            if a:
                bb.name=a
                bb.save()
            bb.save()
            messages.success(request,' Updated successfuly')
    context = {
        "web":web,
        'user':user,
        'last_year':y,
        'manager':manager,
        'b':b,
        'bb':bb,
    }
    return render(request,'manager/blog/edit main blog.html',context)


@login_required(login_url='login')
def addsubblog(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    y = AcademicYear.objects.last().year
    b = Category.objects.all()
    bb = Blog.objects.get(pk=id)
    if request.method == 'POST':
            a = request.POST['name']
            d = request.POST.get('p1')
            e = request.POST.get('p2')
            f = request.POST.get('p3')
            aa = Addblog.objects.create(name=a,blog=bb)
            if d:
                aa.p1=d
            if e:
                aa.p2=e
            if f:
                aa.p3=f
            if request.FILES:
                b = request.FILES['cover']
                aa.Image=b
            aa.save()
            messages.success(request,'New sub blogpost added successfuly')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        'b':b,
        'bb':bb
    }
    return render(request,'manager/blog/add sub blog.html',context)


@login_required(login_url='login')
def editsubblog(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    b = Category.objects.all()
    y = AcademicYear.objects.last().year
    bb = Addblog.objects.get(pk=id)
    if request.method == 'POST':
            a = request.POST['name']
            d = request.POST.get('p1')
            e = request.POST.get('p2')
            f = request.POST.get('p3')
            aa = bb
            aa.name=a
            if d:
                aa.p1=d
            if e:
                aa.p2=e
            if f:
                aa.p3=f
            if request.FILES:
                b = request.FILES['cover']
                aa.Image=b
            aa.save()
            messages.success(request,'sub blogpost Updated successfuly')
    context = {
        "web":web,
        'user':user,
        'last_year':y,
        'manager':manager,
        'b':b,
        'bb':bb
    }
    return render(request,'manager/blog/edit sub blog.html',context)


@login_required(login_url='login')
def deleteblog(request,id):
        b = Blog.objects.get(pk=id)
        b.delete()
        messages.success(request,"Blogpost deleted!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
@login_required(login_url='login')
def deletesubblog(request,id):
        b = Addblog.objects.get(pk=id)
        b.delete()
        messages.success(request,"Sub Blogpost deleted!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
@login_required(login_url='login')
def deletecategoryblog(request,id):
        b = Category.objects.get(pk=id)
        b.delete()
        messages.success(request,"Blogpost Category deleted!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def info(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    y = AcademicYear.objects.last().year
    
    
    #levels
    levels = Level.objects.all()
    if request.method == 'POST':
        if 'updatelevel' in request.POST:
            a = request.POST['name']
            b = request.POST['id']
            bb = Level.objects.get(pk=b)
            bb.name=a
            bb.save()
            messages.success(request,"Selected Academic Level Updated Successfully!")
            return redirect("m_web_info")
        if 'deletelevel' in request.POST:
            b = request.POST['id']
            l = Level.objects.get(pk=b)
            l.delete()
            messages.success(request,"Selected Academic Level Deleted Successfully!")
            return redirect("m_web_info")
        if 'addlevel' in request.POST:
            a = request.POST['name']
            Level.objects.create(name=a)
            messages.success(request,"Selected Academic Level added Successfully!")
            return redirect("m_web_info")
    
    #grades
    grades = Grade.objects.all()
    if request.method == 'POST':
        if 'updategrade' in request.POST:
            a = request.POST['name']
            b = request.POST['id']
            c = request.POST['level']
            ll = Level.objects.get(pk=c)
            bb = Grade.objects.get(pk=b)
            bb.name=a
            bb.level=ll
            bb.save()
            messages.success(request,"Selected Academic Grade Updated Successfully!")
            return redirect("m_web_info")
        if 'deletegrade' in request.POST:
            b = request.POST['id']
            l = Grade.objects.get(pk=b)
            l.delete()
            messages.success(request,"Selected Academic Level Deleted Successfully!")
            return redirect("m_web_info")
        if 'addgrade' in request.POST:
            a = request.POST['name']
            c = request.POST['level']
            ll = Level.objects.get(pk=c)
            if not a:
                messages.error(request,"You have to add something in level name ")
                return redirect("m_web_info")
            else:
                Grade.objects.create(name=a,level=ll)
                messages.success(request, "Academic Grade added Successfully!")
                return redirect("m_web_info")
    
    
    #subjects
    subjects = Subject.objects.all()
    if request.method == 'POST':
        if 'updatesubject' in request.POST:
            a = request.POST['name']
            b = request.POST['id']
            c = request.POST.getlist('grade')
            bb = Subject.objects.get(pk=b)
            bb.name=a
            bb.grade.set(c)
            bb.save()
            messages.success(request,"Selected Subject Updated Successfully!")
            return redirect("m_web_info")
        if 'deletesubject' in request.POST:
            b = request.POST['id']
            l = Subject.objects.get(pk=b)
            l.delete()
            messages.success(request,"Selected subject Deleted Successfully!")
            return redirect("m_web_info")
        if 'addsubject' in request.POST:
            a = request.POST['name']
            c = request.POST['grade']
            if not a:
                messages.error(request,"You have to add something in name ")
                return redirect("m_web_info")
            else:
                aaaa = Subject.objects.create(name=a)
                c = request.POST.getlist('grade')
                aaaa.grade.set(c)
                messages.success(request, "new subject added Successfully!")
                return redirect("m_web_info")
    gradess = Grade.objects.all()
    context = {
        "web":web,
        'last_year':y,
        'user':user,
        'manager':manager,
        'levels':levels,
        'grades':grades,
        'gradess':gradess,
        'subjects':subjects,
    }
    return render(request,'manager/web/info.html',context)


@login_required(login_url='login')
def resultdata(request,year):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    yyy = AcademicYear.objects.get(year=year)
    this_year = AcademicYear.objects.get(year=year).year
    y = AcademicYear.objects.last().year
    gg = Grade.objects.all()
    ss = Subject.objects.all()
    if y == this_year:
        tests = Test.objects.filter(year=yyy)
        grade = Grade.objects.all()
        if request.method == 'POST':
            if 'updatetest' in request.POST:
                name = request.POST['name']
                time = request.POST['term']
                capacity = request.POST['capacity']
                g = request.POST.getlist('grade')
                f = request.POST.getlist('subject')
                id = request.POST['id']
                change = Test.objects.get(pk=id)
                change.time=time
                change.name=name
                change.capacity=capacity
                change.grade.set(g)
                change.save()
                changes = Test.objects.get(pk=id)
                changes.subject.set(f)
                changes.save()
                messages.success(request,'Selected Test updated')
                return redirect('m_data_result',year=year)
            if 'deletetest' in request.POST:
                id = request.POST['id']
                delete = Test.objects.get(pk=id)
                delete.delete()
                messages.success(request,'Selected Test deleted')
                return redirect('m_data_result',year=year)
            if 'addtest' in request.POST:
                name = request.POST['name']
                time = request.POST['term']
                capacity = request.POST['capacity']
                g = request.POST.getlist('grade')
                f = request.POST.getlist('subject')
                change = Test.objects.create(name=name,time=time,capacity=capacity,year=yyy)
                change.grade.set(g)
                change.subject.set(f)
                change.save()
                messages.success(request,'Selected Test added')
                return redirect('m_data_result',year=year)
        context = {
            "web":web,
            'user':user,
            'manager':manager,
            'this':this_year,
            'tests':tests,
            'grade':grade,
            'last_year':y,
            'gg':gg,
            'ss':ss,
        }
        return render(request,'manager/data/result.html',context)
    else:
        year = AcademicYear.objects.get(year=year)
        students = History.objects.filter(academicYear=year)
        context = {
            'students':students,
            'this':this_year,
            'last_year':y,
        }
        return render(request,'manager/data/readonly.html',context)
        
    


@login_required(login_url='login')
def resultdatatest(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    this_year = AcademicYear.objects.last()
    tests = Test.objects.get(id=id)
    result = Result.objects.filter(name=tests)
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        'this':this_year,
        'tests':tests,
        'result':result,
    }
    return render(request,'manager/data/test.html',context)


@login_required(login_url='login')
def resultdatagrade(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    grade = Grade.objects.get(pk=id)
    grades = Grade.objects.all().exclude(id=grade.id)
    this_year = AcademicYear.objects.last()
    students = Student.objects.filter(grade=grade).order_by('first_name','last_name')
    y = AcademicYear.objects.last().year
    sub = Subject.objects.filter(grade=grade)
    subr = SubjectReslut.objects.filter(grade=grade)
    first_stu = StudentStatus.objects.filter(time=this_year).order_by('-first_average')
    second_stu = StudentStatus.objects.filter(time=this_year).order_by('-second_average')
    stu = StudentStatus.objects.filter(time=this_year).order_by('-average')
    sub_count = sub.count()+3
    fff = Student.objects.filter(grade=grade).count()
    for rrr in students:
        for rr in Subject.objects.all():
            if not StudentStatus.objects.filter(student=rrr,time=this_year).exists():
                StudentStatus.objects.create(student=rrr,time=this_year,second_average=0,second_from=0,second_total=0,first_average=0,first_from=0,first_total=0)
                
            if not SubjectReslut.objects.filter(student=rrr,subject=rr,grade=grade,time=this_year).exists():
                SubjectReslut.objects.create(student=rrr,subject=rr,grade=grade,time=this_year,second=0,first=0)
    if request.method == 'POST':
        if 'pass_single_default' in request.POST:
            id = request.POST['id']
            g = request.POST['grade']
            gg = Grade.objects.get(pk=g)
            sttu = Student.objects.get(pk=id)
            student=sttu
            save_all_student_history()
            student.profile.grade=gg
            student.grade=gg.name
            student.save()
            for bbb in Result.objects.filter(student=student):
                bbb.delete()
            messages.success(request,'Student passed to grade ' + gg.name)
            return redirect('m_data_result_grade',grade.id)
        if 'pass_all_default' in request.POST:
            save_all_student_history()
            for bbbbb in Student.objects.filter(grade=grade):
                g = request.POST['grade']
                gg = Grade.objects.get(pk=g)
                studentt=bbbbb
                studentt.profile.grade=gg
                studentt.grade=gg.name
                studentt.save()
                for bbb in Result.objects.filter(student=studentt):
                    bbb.delete()
            messages.success(request,'Students passed to grade ' + gg.name)
            return redirect('m_data_result_grade',grade.id)   
        if 'pass_single' in request.POST:
            id = request.POST['id']
            g = request.POST['grade']
            gg = Grade.objects.get(pk=g)
            sttu = Student.objects.get(pk=id)
            student=sttu
            for bbb in Result.objects.filter(student=student):
                bbb.delete()
            for a in SubjectReslut.objects.filter(student=student):
                a.delete()
            StudentStatus.objects.get(student=student).delete()
            student.profile.grade=gg
            student.grade=gg.name
            student.save()
            for bbb in Result.objects.filter(student=student):
                bbb.delete()
            messages.success(request,'Student passed to grade ' + gg.name + ' Without saving any data')
            return redirect('m_data_result_grade',grade.id)
        if 'pass_all_single' in request.POST:
            for bbbbbb in Student.objects.filter(grade=grade):
                g = request.POST['grade']
                gg = Grade.objects.get(pk=g)
                sttu = bbbbbb
                student=sttu
                for bbb in Result.objects.filter(student=student):
                    bbb.delete()
                for a in SubjectReslut.objects.filter(student=student):
                    a.delete()
                StudentStatus.objects.get(student=student).delete()
                student.profile.grade=gg
                student.grade=gg.name
                student.save()
                for bbb in Result.objects.filter(student=student):
                    bbb.delete()
                messages.success(request,'Student passed to grade ' + gg.name + ' Without saving any data')
                return redirect('m_data_result_grade',grade.id)
        if 'fail_single_default' in request.POST:
            id = request.POST['id']
            sttu = Student.objects.get(pk=id)
            student=sttu
            for bbb in Result.objects.filter(student=student):
                bbb.delete()
            save_all_student_history()
            student.save()
            for bbb in Result.objects.filter(student=student):
                bbb.delete()
            messages.success(request,'Student is still in grade ' + grade.name)
            return redirect('m_data_result_grade',grade.id)
        if 'fail_single' in request.POST:
            id = request.POST['id']
            sttu = Student.objects.get(pk=id)
            student=sttu
            for bbb in Result.objects.filter(student=student):
                bbb.delete()
            for a in SubjectReslut.objects.filter(student=student):
                a.delete()
            StudentStatus.objects.get(student=student).delete()
            student.save()
            for bbb in Result.objects.filter(student=student):
                bbb.delete()
            messages.success(request,'Student data reseted wihout saving data student is still in grade ' + grade.name)
            return redirect('m_data_result_grade',grade.id)
        if 'fail_all_single' in request.POST:
            for bbbbbb in Student.objects.filter(grade=grade):
                sttu = bbbbbb
                student=sttu
                for bbb in Result.objects.filter(student=student):
                    bbb.delete()
                for a in SubjectReslut.objects.filter(student=student):
                    a.delete()
                StudentStatus.objects.get(student=student).delete()
                student.save()
                for bbb in Result.objects.filter(student=student):
                    bbb.delete()
            messages.success(request,'Student data reseted wihout saving data student is still in grade ' + grade.name)
            return redirect('m_data_result_grade',grade.id)
        
        
        
    context = {
        "web":web,
        'grades':grades,
        'user':user,
        'manager':manager,
        'this':this_year,
        'grade':grade, 
        'last_year':y,
        'sub':sub,
        'students':students,
        'subr':subr,
        'stu':stu,
        'fstu':first_stu,
        'sstu':second_stu,
        'fff':fff,
        'subb':sub_count,
    }
    return render(request,'manager/data/grade data.html',context)


def resultdatastudent(request,id,year):
    web = Webpack.objects.get(pk=1)
    this_year = AcademicYear.objects.get(year=year)
    student = Student.objects.get(id=id)
    site = get_current_site(request)
    if StudentStatus.objects.filter(student=student,time=this_year).exists():
        stat = StudentStatus.objects.get(student=student,time=this_year)
        fff = Student.objects.filter(grade=student.profile.grade).count()
    else:
        stat=None
        fff=None
    subr = SubjectReslut.objects.filter(grade=student.profile.grade.id,time=this_year,student=student)
    if request.method=='POST':
        fr = request.POST['f_rank']
        sr = request.POST['s_rank']
        r = request.POST['rank']
        c = StudentStatus.objects.get(student=student,time=this_year)
        c.first_rank=fr
        c.second_rank=sr
        c.rank=r
        c.save()
        return redirect('m_data_result_student' ,student.id ,year)
    context = {
        "web":web,
        'this':this_year,
        'student':student,
        'fff':fff,
        'stat':stat,
        'subr':subr,
        'site':site,
        'id':id,
        'year':year,
    }
    return render(request,'manager/data/grade student.html',context)




@login_required(login_url='login')
def resultdataterm(request,name):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    this_year = AcademicYear.objects.last()
    y = AcademicYear.objects.last().year
    if name == 'first':
        a = 'first academic term'
    elif name == 'second':
        a = 'second academic term'
    result = Result.objects.filter(time=a)
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'this':this_year,
        'tests':a,
        'result':result,
        'last_year':y,
    }
    return render(request,'manager/data/grade.html',context)

@login_required(login_url='login')
def resultdataall(request,year):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    this_year = AcademicYear.objects.last()
    y = AcademicYear.objects.last().year
    result = Result.objects.filter(time=this_year)
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'this':this_year,
        'result':result,
        'last_year':y,
    }
    return render(request,'manager/data/grade.html',context)


@login_required(login_url='login')
def time(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    years = AcademicYear.objects.all()
    year = years.last()
    students = Student.objects.filter(year=year)
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        if 'updateyear' in request.POST:
            a = request.POST['name']
            id = request.POST['id']
            aa = AcademicYear.objects.get(id=id)
            aa.year=a
            aa.save()
            messages.success(request,'Updated')
    context = {
        "web":web,
        'user':user,
        'last_year':y,
        'manager':manager,
        'years':years,
        'year':year,
        'students':students,
    }
    return render(request,'manager/time.html',context)



@login_required(login_url='login')
def savetime(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    Year = AcademicYear.objects.get(id=id)
    
    
    AcademicYear.objects.create(year=Year.year+1)
    laststudent(request)
    messages.success(request,"All data saved successfully And The year is added")
    return redirect('m_time')


@login_required(login_url='login')
def resultdatahistory(request,id,year):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    us = User.objects.get(id=id)
    p = Profile.objects.get(user=us)
    st = Student.objects.get(profile=p)
    a = AcademicYear.objects.get(year=year)
    tests = TestHistory.objects.filter(academicYear=a)
    result = ResultHistory.objects.filter(student=st)
    y = AcademicYear.objects.last().year
    context = {
        "web":web,
        'user':user,
        'last_year':y,
        'manager':manager,
        'result':result,
        'test':tests
    }
    return render(request,'manager/data/history.html',context)


@login_required(login_url='login')
def laststudent(request):
    a = AcademicYear.objects.last()
    for b in Student.objects.all():
        b.year=a
        b.save()
        messages.success(request,"All Stuents Are transfered to this year")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def profile(request):
    web = Webpack.objects.get(pk=1)
    me = request.user
    pp = Profile.objects.get(user=me)
    manager = Manager.objects.get(profile=pp)
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        
            if 'update' in request.POST:
                first_name = request.POST['firstName']
                last_name = request.POST['lastName']
                email = request.POST['email']
                username = request.POST['username']
                phone = request.POST['phone']
                facebook = request.POST['instagram']
                telegram = request.POST['telegram']
                p1 = request.POST['password1']
                p2 = request.POST['password2']
                if Password.objects.filter(of=me).exists():
                    p = Password.objects.get(of=me)
                if request.FILES:
                    profile_pic = request.FILES['profile_pic']
                    manager.profile_pic = profile_pic
                    manager.save()
                    messages.success(request,'Your Profile Picture is Updated Successfully!')
                if p1:
                    if p1 != p2:
                        messages.error(request,"Passwords donot match!")
                    elif len(p1) < 8:
                        messages.error(request,"Password is too short it must be grater than 8 characters!")
                    else:
                        me.set_password(p1)
                        me.save()
                        p.password=p1
                        p.save()
                        messages.success(request,"Password Changed Successfully")
                        return redirect('logout')
                if username:
                    if me.username != username:
                        if User.objects.filter(username=username).exists():
                            messages.error(request,"username is already in use please change it!")
                        else:
                            me.username=username
                            manager.username=username
                            manager.save()
                            me.save()
                            messages.success(request,'Username Updated Succesfully')
                if first_name or last_name:
                    if not User.objects.filter(first_name=first_name,last_name=last_name).exists():
                        me.first_name=first_name
                        me.last_name=last_name
                        me.save()
                        p.first_name=first_name
                        p.last_name=last_name
                        p.save()
                        manager.first_name = first_name
                        manager.last_name = last_name
                        manager.save()
                        messages.success(request,"Your name is updated successfully")
                if email:
                    if not User.objects.filter(email=email).exists():
                        me.email = email
                        p.email = email
                        me.save()
                        p.save()
                        messages.success(request,"Email Updated Successfully")
                if phone:
                    if pp.phone != phone:
                        if Profile.objects.filter(phone=phone).exists():
                            messages.error(request,"Phone Number is in Use please change it!")
                        else:
                            pp.phone=phone
                            p.phone=phone
                            pp.save()
                            p.save()
                            messages.success(request,'Phone Number updated Successfully')
                if telegram:
                    if not Manager.objects.filter(telegram=telegram).exists():
                        manager.telegram=telegram
                        manager.save()
                        messages.success(request,'Your Telegram url is updated Successfully!')
            if 'delete' in request.POST:
                me.delete()
                messages.success(request,"Hey Dear user glad to work with you thank you for everything good bye!")
                return redirect('r_index')
      
    context = {
        'last_year':y,
        "web":web,
        'user':me,
        'manager':manager,
    }
    return render(request,'manager/profile.html',context)




@login_required(login_url='login')
def event(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    events = Event.objects.all()
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        if 'add' in request.POST:
            a = request.POST['name']
            Event.objects.create(name=a)
            messages.success(request,'Events added')
            return redirect('m_event')
        if 'update' in request.POST:
            a = request.POST['name']
            b = request.POST['id']
            c = Event.objects.get(pk=b)
            c.name=a
            c.save()
            messages.success(request,'Events updated')
            return redirect('m_event')
        if 'delete' in request.POST:
            b = request.POST['id']
            c = Event.objects.get(pk=b)
            c.delete()
            messages.success(request,'Events deleted')
            return redirect('m_event')
    context = {
        "web":web,
        'user':user,
        'last_year':y,
        'manager':manager,
        'events':events,
    }
    return render(request,'manager/event.html',context)



@login_required(login_url='login')
def gallery(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    event = Event.objects.get(pk=id)
    galleries = Gallery.objects.filter(event=event)
    y = AcademicYear.objects.last().year
    if request.method == 'POST':
        if 'add' in request.POST:
            if request.FILES:
                a = request.FILES['file']
                b = request.POST['name']
                Gallery.objects.create(image=a,name=b,event=event,on_front=True)
                messages.success(request,'picture added')
        if 'update' in request.POST:
            a = request.POST['id']
            b = request.POST['name']
            c = Gallery.objects.get(pk=a)
            c.name=b
            c.save()
            messages.success(request,'picture updated')
        if 'delete' in request.POST:
            a = request.POST['id']
            c = Gallery.objects.get(pk=a)
            c.delete()
            messages.success(request,'picture deleted')
    context = {
        "web":web,
        'user':user,
        'manager':manager,
        'last_year':y,
        'event':event,
        'g':galleries,
    }
    return render(request,'manager/gallery.html',context)





def save_all_student_history():
    studentt = Student.objects.all()
    for a in studentt:
        if not History.objects.filter(user=a.profile.user,academicYear=a.year).exists():
            h = History.objects.create(
            user=a.profile.user,
            academicYear=a.year,
            first_name=a.profile.user.first_name,
            last_name=a.profile.user.last_name,
            username=a.profile.user.username,
            nationality=a.nationality,
            city=a.city,
            phone=a.profile.phone,
            sex=a.profile.sex,
            level=a.profile.level,
            grade=a.profile.grade,
            )
            for b in Test.objects.filter(year=AcademicYear.objects.last()):
                test = b
                t = TestHistory.objects.create(
                name=test.name,
                history=h,
                capacity=test.capacity,
                time=test.time,
                academicYear=a.year,
            )
                for c in Result.objects.filter(name=test):
                    result=c
                    ResultHistory.objects.create(
                    status=result.status,
                    name=t,
                    history=h,
                    subjects=result.subject,
                    student=a,
                    time=result.time,
                    year=a.year
                )
            for b in SubjectReslut.objects.filter(student=a):
                SubjectReslutHistory.objects.create(
                        first=b.first,
                        f_from=b.f_from,
                        s_from=b.f_from,
                        second=b.second,
                        subject=b.subject,
                        student=h,
                        time=b.time,
                    )
            sst = StudentStatus.objects.get(student=a,time=AcademicYear.objects.last())
            StudentStatusHistory.objects.create(
                    first_total=sst.first_total,
                    first_from=sst.first_from,
                    first_average=sst.first_average,
                    second_total=sst.second_total,
                    second_from=sst.second_from,
                    second_average=sst.second_average,
                    average=sst.average,
                    first_rank=sst.first_rank,
                    second_rank=sst.second_rank,
                   rank=sst.rank,
                    student=h,
                    time=sst.time
                )
            
    
    
    
    
@login_required(login_url='login')
def HomeRooms(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    manager = Manager.objects.get(profile=pp)
    this_year = AcademicYear.objects.last()
    y = AcademicYear.objects.last().year
    home = HomeRoom.objects.filter(year=y)
    teachers = Teacher.objects.all()
    grades = Grade.objects.all()
    if request.method == 'POST':
        if 'add' in request.POST:
            a=request.POST['teacher']
            b = request.POST['grade']
            if HomeRoom.objects.filter(teacher=Teacher.objects.get(id=a)).exists():
                messages.error(request,'requested teacher already has his own room please add another')
                
            elif HomeRoom.objects.filter(room=Grade.objects.get(id=b)).exists():
                messages.error(request,'requested Room already has his own teacher please change it')
            else:
                HomeRoom.objects.create(teacher=Teacher.objects.get(pk=a),room=Grade.objects.get(pk=b),year=y)
                messages.success(request,'Added!')
                return redirect("m_room")
        if 'update' in request.POST:
            a=request.POST['teacher']
            b = request.POST['grade']
            id=request.POST['id']
            if HomeRoom.objects.filter(teacher=Teacher.objects.get(id=a)).exists():
                messages.error(request,'requested teacher already has his own room please add another')
                
            elif HomeRoom.objects.filter(room=Grade.objects.get(id=b)).exists():
                messages.error(request,'requested Room already has his own teacher please change it')
            else:
                c=HomeRoom.objects.get(id=id)
                c.teacher=Teacher.objects.get(id=a)
                c.grade=Grade.objects.get(pk=b)
                c.save()
                messages.success(request,'Updated!')
                return redirect("m_room")
        if 'delete' in request.POST:
            id=request.POST['id']
            c=HomeRoom.objects.get(id=id)
            c.delete()
            messages.success(request,'deleted!')
            return redirect("m_room")
    context = {
        "web":web,
        'user':user,
        'teachers':teachers,
        'grades':grades,
        'manager':manager,
        'this':this_year,
        'last_year':y,
        'home':home,
    }
    return render(request,'manager/home room.html',context)

