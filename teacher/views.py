from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from home.models import *
from student.models import *
from .models import *
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Sum
from redirector.models import *
from django.template import Template, Context
from staff.models import Staff


@login_required(login_url='login')
def index(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    student = Student.objects.all().order_by('grade','first_name','last_name')
    accept_student = Student.objects.filter(is_verified=False)
    year = AcademicYear.objects.last()
    if request.method == "POST":
        if 'accept' in request.POST:
            id=request.POST['id']
            s = Student.objects.get(id=id)
            s.is_verified=True
            s.save()
            messages.success(request,"User accepted")
        if 'delete' in request.POST:
            id=request.POST['id']
            s = Student.objects.get(id=id)
            s.profile.user.delete()
            messages.success(request,"User deleted")
        if 'generate' in request.POST:
            if year.start == True:
                year.start = False
            else:
                year.start = True
            year.save()
            GenerateSchool(user.id)
            messages.success(request,"Change made successfully")
            return redirect('r_index')
    context = {
        "web":web,
        'user':user,
        'teacher':teacher,
        'student':student,
        'accept':accept_student,
        'year':year,
    }
    return render(request,'teacher/index.html',context)

def saveresult(request):
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    if request.method=='POST':
        id1 = request.POST['student_id']
        student = Student.objects.get(pk=id1)
        id2 = request.POST['test_id']
        test = Test.objects.get(id=id2)
        id3 = request.POST['result_id']
        input = request.POST['input']
        if 'update' in request.POST:
            up = Result.objects.get(pk=id3)
            up.status = input
            up.save()
            id = up.subject.id
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def GenerateSchool(idd):
    web = Webpack.objects.get(pk=1)
    user = User.objects.get(id=idd)
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    asx='f'
    y = AcademicYear.objects.last()
    totalll = None
    totall = None
    stat = StudentStatus.objects.filter(time=y)
    subs = SubjectReslut.objects.filter(time=y,subject=teacher.subject)
    
    for ggg in Grade.objects.all():
        student = Student.objects.filter(grade=ggg.name,is_verified=True,new=False)
        test = Test.objects.filter(grade=ggg,subject=teacher.subject,time="second academic term",year=y)
        result = Result.objects.filter(subject=teacher.subject,time="second academic term",year=y)
        for s in Student.objects.filter(grade=ggg.name,is_verified=True,new=False):
                st = Student.objects.get(pk=s.id)
                for t in test:
                    tt = Test.objects.get(pk=t.id)
                    for su in Subject.objects.all():
                        ss = Subject.objects.get(pk=su.id)
                        if not Result.objects.filter(student=st,name=tt,subject=ss,time="second academic term"):
                            Result.objects.create(subject=ss,year=y,student=st,time="second academic term",name=tt,status="0")
        
    
    for ggg in Grade.objects.all():
        student = Student.objects.filter(grade=ggg.name,is_verified=True,new=False)
        test = Test.objects.filter(grade=ggg,subject=teacher.subject,time="first academic term",year=y)
        result = Result.objects.filter(subject=teacher.subject,time="first academic term",year=y)
        for s in Student.objects.filter(grade=ggg.name,is_verified=True,new=False):
            st = Student.objects.get(pk=s.id)
            for t in test:
                tt = Test.objects.get(pk=t.id)
                for su in Subject.objects.all():
                    ss = Subject.objects.get(pk=su.id)
                    if not Result.objects.filter(student=st,name=tt,subject=ss,time="first academic term",year=AcademicYear.objects.last()):
                        Result.objects.create(subject=ss,year=y,student=st,time="first academic term",name=tt,status="0")
        for rrr in student:
                    total = Result.objects.filter(student=rrr,time="first academic term",year=AcademicYear.objects.last()).aggregate(Sum('status'))['status__sum']
                    totalll = Result.objects.filter(student=rrr,subject=teacher.subject,time="first academic term",year=AcademicYear.objects.last()).aggregate(Sum('status'))['status__sum']
                    totall = test.aggregate(Sum('capacity'))['capacity__sum']
                    gra = Grade.objects.get(id=rrr.profile.grade.id)
                    g = Subject.objects.filter(grade=gra)
                    if totall:
                        tot = (totall * g.count())
                        if tot != 0 :
                            average = (total/tot)*100
                        else:
                            average = (0/1)*100
                    else:
                        tot = (0 * g.count())
                        average = (total/1)*100
                    rrr.average = average
                    rrr.save()
                    ggg = Grade.objects.get(name=rrr.grade)
                    if StudentStatus.objects.filter(student=rrr,time=y).exists():
                        aaaa = StudentStatus.objects.get(student=rrr,time=y)
                        aaaa.first_average=average
                        aaaa.first_from=tot
                        aaaa.first_total=total
                        if aaaa.first_total and aaaa.second_total:
                            aaaa.average=((aaaa.first_total+aaaa.second_total)/(aaaa.first_from+aaaa.second_from))*100
                        else:
                            average=0
                        aaaa.save()
                    else:
                        StudentStatus.objects.create(student=rrr,time=y,first_average=average,first_from=tot,first_total=total)
                    if SubjectReslut.objects.filter(student=rrr,subject=teacher.subject,grade=ggg,time=y).exists():
                        sss = SubjectReslut.objects.get(student=rrr,subject=teacher.subject,grade=ggg,time=y)
                        sss.first = totalll
                        sss.f_from = totall
                        sss.save()
                    else:
                        SubjectReslut.objects.create(student=rrr,subject=teacher.subject,grade=ggg,time=y,first=total,f_from=totall)
        
        for rrr in student:
                total = Result.objects.filter(student=rrr,time="second academic term",year=AcademicYear.objects.last()).aggregate(Sum('status'))['status__sum']
                totalll = Result.objects.filter(student=rrr,subject=teacher.subject,time="second academic term",year=AcademicYear.objects.last()).aggregate(Sum('status'))['status__sum']
                totall = test.aggregate(Sum('capacity'))['capacity__sum']
                gra = Grade.objects.get(id=rrr.profile.grade.id)
                g = Subject.objects.filter(grade=gra)
                if totall:
                    tot = (totall * g.count())
                    if tot and total:
                        if tot != 0 or tot is not None :
                            average = (total/tot)*100
                        else:
                            average = (0/1)*100
                else:
                    tot = (0 * g.count())
                    average = (total/1)*100
                rrr.average = average
                rrr.save()
                ggg = Grade.objects.get(name=rrr.grade)
                if StudentStatus.objects.filter(student=rrr,time=y).exists():
                    aaaa = StudentStatus.objects.get(student=rrr,time=y)
                    aaaa.second_average=average
                    aaaa.second_from=tot
                    aaaa.second_total=total
                    if aaaa.first_total and aaaa.second_total:
                        aaaa.average = ((aaaa.first_total+aaaa.second_total)/(aaaa.first_from+aaaa.second_from))*100
                    else:
                        average=0
                    aaaa.save()
                else:
                    StudentStatus.objects.create(student=rrr,time=y,second_average=average,second_from=tot,second_total=total)
                if SubjectReslut.objects.filter(student=rrr,subject=teacher.subject,grade=ggg,time=y).exists():
                    sss = SubjectReslut.objects.get(student=rrr,subject=teacher.subject,grade=ggg,time=y)
                    sss.second = totalll
                    sss.s_from = totall
                    sss.save()
                else:
                    SubjectReslut.objects.create(student=rrr,subject=teacher.subject,grade=ggg,time=y,second=total,s_from=totall)
             
        

@login_required(login_url='login')
def oneresults(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    asx='f'
    grade = Grade.objects.get(pk=id)
    y = AcademicYear.objects.last()
    totalll = None
    totall = None
    stat = StudentStatus.objects.filter(time=y)
    subs = SubjectReslut.objects.filter(time=y,subject=teacher.subject)
    if Teacher.objects.filter(profile=pp,my_room=grade).exists():
        student = Student.objects.filter(grade=grade.name,is_verified=True,new=False)
        test = Test.objects.filter(grade=grade,subject=teacher.subject,time="first academic term",year=y)
        result = Result.objects.filter(subject=teacher.subject,time="first academic term",year=y)
        if request.method == 'POST':
            if 'test_add' in request.POST:
                amount = request.POST['amount']
                stu = request.POST['student']
                stt = Student.objects.get(id=stu)
                tes = request.POST['test']
                ttt = Test.objects.get(id=tes)
                sub = request.POST['subject']
                rr = Result.objects.get(name=ttt,subject=teacher.subject,student=stt,time="first academic term")
                rr.status = amount
                rr.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if 'mass' in request.POST:
                testt = request.POST['testname']
                tt = Test.objects.get(id=testt)
                for aaaa in student:
                    a = request.POST[aaaa.username]
                    aa = Result.objects.get(name=tt,subject=teacher.subject,student=aaaa,time="first academic term")
                    aa.status=a
                    aa.save()
        
    else:return HttpResponse("This is not you class what are you doing here?")
    context = {
        "web":web,
        'user':user,
        'teacher':teacher,
        'student':student,
        'test':test,
        'result':result,
        'grade':grade,
        'total':totalll,
        'totall':totall,
        'stat':stat,
        'asx':asx,
        'subs':subs,
    }
    return render(request,'teacher/result.html',context)


@login_required(login_url='login')
def tworesults(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    y = AcademicYear.objects.last()
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    grade = Grade.objects.get(pk=id)
    totalll = None
    totall = None
    asx=None
    stat = StudentStatus.objects.filter(time=y)
    subs = SubjectReslut.objects.filter(time=y,subject=teacher.subject)
    if Teacher.objects.filter(profile=pp,my_room=grade).exists():
        student = Student.objects.filter(grade=grade.name,is_verified=True,new=False)
        test = Test.objects.filter(grade=grade,subject=teacher.subject,time="second academic term",year=y)
        result = Result.objects.filter(subject=teacher.subject,time="second academic term",year=y)
        if request.method == 'POST':
            if 'test_add' in request.POST:
                amount = request.POST['amount']
                stu = request.POST['student']
                stt = Student.objects.get(id=stu)
                tes = request.POST['test']
                ttt = Test.objects.get(id=tes)
                sub = request.POST['subject']
                rr = Result.objects.get(name=ttt,subject=teacher.subject,student=stt,time="second academic term")
                rr.status = amount
                rr.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if 'mass' in request.POST:
                testt = request.POST['testname']
                tt = Test.objects.get(id=testt)
                for aaaa in student:
                    a = request.POST[aaaa.username]
                    aa = Result.objects.get(name=tt,subject=teacher.subject,student=aaaa,time="second academic term")
                    aa.status=a
                    aa.save()
                  
    else:return HttpResponse("This is not you class what are you doing here?")
    context = {
        "web":web,
        'user':user,
        'teacher':teacher,
        'student':student,
        'test':test,
        'result':result,
        'grade':grade,
        'total':totalll,
        'totall':totall,
        'asx':asx,
        'stat':stat,
        'subs':subs,
    }
    return render(request,'teacher/result.html',context)

@login_required(login_url='login')
def addpost(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    grade = Grade.objects.all()
    if request.method == 'POST':
        a = request.POST['for']
        gr = Grade.objects.get(pk=a)
        b = request.POST['title']
        c = request.POST['disc']
        d = request.POST['link1']
        e = request.POST['link2']
        f = request.POST['link3']
        if not request.FILES:
            GradePost.objects.create(for_grade=gr,title=b,disc=c,link1=d,link2=e,link3=f,teacher=teacher)
            messages.success(request,'Message Posted Successufully')
        else:
            try:
                if 'file1' in request.FILES:
                    g = request.FILES['file1']
                    GradePost.objects.create(for_grade=gr,title=b,disc=c,link1=d,link2=e,link3=f,file1=g,teacher=teacher)
                    messages.success(request,'Message Posted Successufully')
                elif 'file2' in request.FILES:
                    h = request.FILES['file2']
                    GradePost.objects.create(for_grade=gr,title=b,disc=c,link1=d,link2=e,link3=f,file1=g,teacher=teacher,file2=h)
                    messages.success(request,'Message Posted Successufully')
                else:
                    i = request.FILES['file3']
                    GradePost.objects.create(for_grade=gr,title=b,disc=c,link1=d,link2=e,link3=f,file1=g,teacher=teacher,file2=h,file3=i)
                    messages.success(request,'Message Posted Successufully')
            except:messages.error(request,'Error is occured in your files please add them by order')
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
        'grade':grade,
    }
    return render(request,'teacher/add post.html',context)


@login_required(login_url='login')
def addcourse(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    if request.method == 'POST':
        b = request.POST['name']
        c = request.POST['disc']
        if 'cover' in request.FILES:
            a = request.FILES['cover']
            if 'video' in request.FILES:
                d = request.FILES['video']
                aa = Course.objects.create(name=b,cover=a,about=c,video=d,posted_by=teacher)
                aa.subject.add(teacher.subject)
                aa.save()
                messages.success(request,'Course posted!')
            elif 'link' in request.POST:
                d = request.POST['link']
                aa = Course.objects.create(name=b,cover=a,about=c,link=d,posted_by=teacher)
                aa.subject.add(teacher.subject)
                aa.save()
                messages.success(request,'Course posted!')
        else:messages.error(request,'The Cover picture is neccesary')
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
    }
    return render(request,'teacher/add course.html',context)


@login_required(login_url='login')
def addbook(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    if request.method == 'POST':
        b = request.POST['name']
        c = request.POST['disc']
        e = request.POST['author']
        if request.FILES:
            a = request.FILES['cover']
            d = request.FILES['file']
            Library.objects.create(name=b,cover=a,file=d,author=e,disc=c,posted_by=pp)
            messages.success(request,"Book posted succesfully")
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
    }
    return render(request,'teacher/add book.html',context)


@login_required(login_url='login')
def editbook(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    l = Library.objects.get(pk=id)
    if request.method == 'POST':
        b = request.POST['name']
        c = request.POST['disc']
        e = request.POST['author']
        messages.success(request,"Book updated succesfully")
        l.name=b
        l.disc=c
        l.author=e
        l.save()
        if request.FILES:
            if 'cover' in request.FILES:
                d = request.FILES['cover']
                l.cover=d
                l.save()
            if 'file' in request.FILES:
                d = request.FILES['file']
                l.file=d
                l.save()
    context = {
        'web':web,
        'user':user,
        'l':l,
        'teacher':teacher,
    }
    return render(request,'teacher/channel/my-book.html',context)


@login_required(login_url='login')
def channel(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    course = Course.objects.filter(posted_by=teacher).order_by('name')
    search = None
    if request.method == 'POST':
        search = request.POST['tsearch']
        course = Course.objects.filter(posted_by=teacher,name__icontains=search).order_by('name')
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
        'course':course,
        'search':search,
    }
    return render(request,'teacher/channel/channel.html',context)

@login_required(login_url='login')
def editcourse(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    course = Course.objects.get(pk=id)
    if request.method == 'POST':
        b = request.POST['name']
        c = request.POST['disc']
        course.name=b
        course.about=c
        course.save()
        if 'cover' in request.FILES:
            a = request.FILES['cover']
            course.cover=a
            course.save()
        if ('video' in request.FILES) and ('link' in request.POST):
            messages.error(request,"You can't add both video and link at once you have to choose one.")
        elif 'video' in request.FILES:
            d = request.FILES['video']
            course.video=d
            course.link=None
            course.save()
            messages.success(request,'Course updated!')
        elif 'link' in request.POST:
            z = request.POST['link']
            course.link=z
            course.video=None
            course.save()
            messages.success(request,'Course updated!')
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
        'course':course,
    }
    return render(request,'teacher/channel/edit-video.html',context)

@login_required(login_url='login')
def deletecourse(request):
    if request.method == 'POST':
        if 'deletecourse' in request.POST:
            id = request.POST['id']
            course = Course.objects.get(id=id)
            course.delete()
            messages.success(request,'Course deleted Succesfully ')
            return redirect('t_channel')
        if 'deletemessage' in request.POST:
            id = request.POST['id']
            course = GradePost.objects.get(id=id)
            course.delete()
            messages.success(request,'Meassage deleted Succesfully ')
            return redirect('t_message')
        if 'deletebook' in request.POST:
            id = request.POST['id']
            course = Library.objects.get(id=id)
            course.delete()
            messages.success(request,'Selected Book deleted Succesfully ')
            return redirect('t_book')


@login_required(login_url='login')
def myvideo(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    course = Course.objects.get(pk=id)
    c = CourseComment.objects.filter(course=course)
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
        'course':course,
        'c':c,
    }
    return render(request,'teacher/channel/my-video.html',context)

@login_required(login_url='login')
def message(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    grade = GradePost.objects.filter(teacher=teacher)
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
        'grade':grade,
    }
    return render(request,'teacher/channel/messsage.html',context)

@login_required(login_url='login')
def editmessage(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    gg = GradePost.objects.get(pk=id)
    grade = Grade.objects.all().exclude(id=gg.for_grade.id)
    if request.method == 'POST':
        a = request.POST['for']
        gr = Grade.objects.get(pk=a)
        b = request.POST['title']
        c = request.POST['disc']
        messages.success(request,'Message Updated Successufully')
        if 'link1' in request.POST:
            d = request.POST['link1']
            gg.link1=d
            gg.save()
        if 'link2' in request.POST:
            d = request.POST['link2']
            gg.link2=d
            gg.save()
        if 'link3' in request.POST:
            d = request.POST['link3']
            gg.link3=d
            gg.save()
        if request.FILES:
            try:
                if 'file1' in request.FILES:
                    g = request.FILES['file1']
                    gg.file1=g
                    gg.save()
                if 'file2' in request.FILES:
                    g = request.FILES['file2']
                    gg.file2=g
                    gg.save()
                if 'file3' in request.FILES:
                    g = request.FILES['file3']
                    gg.file3=g
                    gg.save()
            except:messages.error(request,'Error is occured in your files please add them by order')
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
        'gg':gg,
        'grade':grade,
    }
    return render(request,'teacher/channel/my-message.html',context)


@login_required(login_url='login')
def books(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    lib = Library.objects.filter(posted_by=pp)
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
        'lib':lib,
    }
    return render(request,'teacher/channel/book.html',context)



@login_required(login_url='login')
def all(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    context = {
        'web':web,
        'user':user,
        'teacher':teacher,
    }
    return render(request,'teacher/all class.html',context)


@login_required(login_url='login')
def TeacherProfile(request):
    web = Webpack.objects.get(pk=1)
    me = request.user
    event = Event.objects.all()
    pp = Profile.objects.get(user=me)
    teacher = Teacher.objects.get(profile=pp)
    sub = Subject.objects.all().exclude(id=teacher.subject.id)
    if request.method == 'POST':
        
            if 'update' in request.POST:
                first_name = request.POST['firstName']
                last_name = request.POST['lastName']
                email = request.POST['email']
                username = request.POST['username']
                phone = request.POST['phone']
                facebook = request.POST['facebook']
                telegram = request.POST['telegram']
                p1 = request.POST['password1']
                p2 = request.POST['password2']
                subject = request.POST['subject']
                sbj = Subject.objects.get(pk=subject)
                p = Password.objects.get(of=me)
                if request.FILES:
                    profile_pic = request.FILES['profile_pic']
                    teacher.profile_pic = profile_pic
                    teacher.save()
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
                            teacher.username=username
                            teacher.save()
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
                        teacher.first_name = first_name
                        teacher.last_name = last_name
                        teacher.save()
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
                if facebook:
                    if not Teacher.objects.filter(facebook=facebook).exists():
                        teacher.facebook=facebook
                        teacher.save()
                        messages.success(request,"Your Facebook address updated Successfully!")
                if telegram:
                    if not Teacher.objects.filter(telegram=telegram).exists():
                        teacher.telegram=telegram
                        teacher.save()
                        messages.success(request,'Your Telegram url is updated Successfully!')
                if subject:
                    if not Teacher.objects.filter(subject=sbj).exists():
                        teacher.subject=sbj
                        teacher.save()
                        messages.success(request,"The change in your subject is saved successfully!")
            if 'delete' in request.POST:
                me.delete()
                messages.success(request,"Hey Dear user glad to work with you thank you for everything good bye!")
                return redirect('r_index')
        
    context = {
        "web":web,
        'event':event,
        'user':me,
        'teacher':teacher,
        'sub':sub,
    }
    return render(request,'teacher/profile.html',context)




@login_required(login_url='login')
def room(request,teacher):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    teacher = Teacher.objects.get(profile=pp)
    if HomeRoom.objects.filter(teacher=Teacher.objects.get(pk=teacher.id)).exists():
        my_room = HomeRoom.objects.get(teacher=teacher)
        students = Student.objects.filter(is_verified=True,grade=my_room.room,new=False).order_by('first_name','last_name')
        stats = StudentStatus.objects.filter(time=AcademicYear.objects.last())
        subs = SubjectReslut.objects.filter(time=AcademicYear.objects.last())
        grades = Grade.objects.all()
        for x in students:
            student = x
            profile = Profile.objects.get(id=student.profile.id)
            sub = SubjectReslut.objects.filter(student=student,time=student.year)
            for a in sub:
                if  a.second:
                    c = ((a.first)+(a.second))/2
                    a.year = c
                    a.save()
            stat = StudentStatus.objects.get(student=student,time=student.year)
            if stat.first_total is not None and stat.second_total is not None:
                c = ((stat.first_total)+(stat.second_total))/2
                stat.total=c
                stat.save()
            for abc in Profile.objects.filter(grade=profile.grade):
                st = Student.objects.get(profile=abc)
                cba = StudentStatus.objects.get(student=st,time=st.year)
                cba.grade=abc.grade
                cba.save()
            index1 = 1
            for c in range(0,StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-first_average').count()):
                a = StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-first_average')[c]
                a.first_rank = index1
                a.save() 
                if (c+1) < StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-first_average').count():
                    next =  StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-first_average')[c+1]
                    if next.first_average == a.first_average:
                        index1 = index1
                    else:
                        index1=index1+1
            index2 = 1
            for c in range(0,StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-second_average').count()):
                a = StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-second_average')[c]
                a.second_rank = index2
                a.save() 
                if (c+1) < StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-second_average').count():
                    next =  StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-second_average')[c+1]
                    if next.second_average == a.second_average:
                        index2 = index2
                    else:
                        index2=index2+1
            index3=1
            for c in range(0,StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-average').count()):
                a = StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-average')[c]
                a.rank = index3
                a.save() 
                if (c+1) < StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-average').count():
                    next =  StudentStatus.objects.filter(time=student.year,grade=profile.grade).order_by('-average')[c+1]
                    if next.average == a.average:
                        index3 = index3
                    else:
                        index3=index3+1

        design = cardType.objects.all()
        if request.method == 'POST':
            if 'remove' in request.POST:
                a = request.POST['id']
                b = Student.objects.get(id=a)
                b.is_verified = False
                b.save()
                messages.success(request,'Student removed from this grade')
            if 'disable' in request.POST:
                a = request.POST['userid']
                b = User.objects.get(id=a)
                b.is_active = False
                b.save()
                messages.success(request,'Student status disabled temporarily')
            if 'enable' in request.POST:
                a = request.POST['userid']
                b = User.objects.get(id=a)
                b.is_active = True
                b.save()
                messages.success(request,'Student status enabled')
            if 'transfer' in request.POST:
                a = request.POST['userid']
                c = request.POST['grade']
                transferStudent(a,c)
                messages.success(request,'Student Transfered')
            if 'fail' in request.POST:
                a = request.POST['id']
                save_student_history(a)
                b = Student.objects.get(id=a)
                messages.success(request,'Student Failed')
            if 'add' in request.POST:
                a = request.POST['d_name']
                st_name = request.POST.get('d_st_name')
                if st_name == 'on':
                    b = True
                else:
                    b = False
                st_grade = request.POST.get('d_st_grade')
                if st_grade == 'on':
                    c = True
                else:
                    c = False
                sc_icon = request.POST.get('d_sc_icon')
                if sc_icon == 'on':
                    d = True
                else:
                    d = False
                table = request.POST.get('d_table')
                if table == 'on':
                    g = True
                else:
                    g = False
                h = cardType.objects.create(
                    name=a,
                    st_name=b,
                    st_grade=c,
                    sc_icon=d,
                    table=g,
                    user=request.user,
                )
                for cccc in students:
                    pass
                return redirect('t_add_card',cccc.id,h.id,AcademicYear.objects.last().id)
        year = AcademicYear.objects.last()
        context = {
            'web':web,
            'user':user,
            'teacher':teacher,
            'stats':stats,
            'subs':subs,
            'grades':grades,
            'my_room':my_room,
            'students':students,
            'design':design,
            'year':year,
        }
        return render(request,'teacher/room.html',context)
    else:
        messages.error(request,'The managers hasnot given you any room yet.')
        return redirect('r_index')
    
 
def save_student_history(id):
    a = Student.objects.get(id=id)
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
  
    
def transferStudent(id,to):
    user = User.objects.get(pk=id)
    profile = Profile.objects.get(user=user)
    student=Student.objects.get(profile=profile)
    grade = Grade.objects.get(id=to)
    save_student_history(student.id)
    profile.grade=grade
    profile.save()
    student.grade=grade.name
    student.new=False
    student.save()
    
    
@login_required(login_url='login')
def addcard(request,id,id2,id3):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    yyy = AcademicYear.objects.get(id=id3)
    student = Student.objects.get(pk=id)
    profile = Profile.objects.get(id=student.profile.id)
    sub = SubjectReslut.objects.filter(student=student,time=yyy)
    stat = StudentStatus.objects.get(student=student,time=yyy)
    card = cardType.objects.get(id=id2)
    text = Text.objects.filter(cardTable=card) .order_by("-id")
    line = Line.objects.filter(cardTable=card).order_by("-id")
    tt = 0
    name = 0
    grade = 0
    ic = 0
    if CTable.objects.filter(cardTable=card).exists():
        tt = CTable.objects.get(cardTable=card)
    if StudentName.objects.filter(cardTable=card).exists():
        name = StudentName.objects.get(cardTable=card)
    if StudentGrade.objects.filter(cardTable=card).exists():
        grade = StudentGrade.objects.get(cardTable=card)
    if icon.objects.filter(cardTable=card).exists():
        ic = icon.objects.get(cardTable=card)
        
    if request.method == 'POST':
        if 'save' in request.POST:
            num = request.POST['num']
            select = request.POST['select']
            
            card.num=num
            card.select=select
            card.save()
              
            
            
            #table
            if card.table == True:
                table_width = request.POST['width']
                table_height = request.POST['height']
                table_y_axis = request.POST['top']
                table_x_axis = request.POST['right']
                table_name_size = request.POST['size']
                table_name_font = request.POST['family']
                table_num_size = request.POST['nsize']
                table_num_font = request.POST['nfamily']
                table_border = request.POST['border']
                
                if not CTable.objects.filter(cardTable=card).exists():
                    CTable.objects.create(
                        cardTable = card,
                        width = table_width,
                        height = table_height,
                        y_axis = table_y_axis,
                        x_axis = table_x_axis,
                        name_size = table_name_size,
                        name_font = table_name_font,
                        num_size = table_num_size,
                        num_font = table_num_font,
                        border = table_border
                    )
                else:
                    table = CTable.objects.get(cardTable=card)
                    table.width = table_width
                    table.height = table_height
                    table.y_axis = table_y_axis
                    table.x_axis = table_x_axis
                    table.name_size = table_name_size
                    table.name_font = table_name_font
                    table.num_size = table_num_size
                    table.num_font = table_num_font
                    table.border = table_border
                    table.save()
                
            #name
            if card.st_name == True:
                st_name_y_axis = request.POST['nametop']
                st_name_x_axis = request.POST['nameright']
                st_name_name_size = request.POST['namesize']
                st_name_name_font = request.POST['namefamily']
    
    
                if not StudentName.objects.filter(cardTable=card).exists():
                    StudentName.objects.create(
                        cardTable=card,
                        y_axis = st_name_y_axis,
                        x_axis = st_name_x_axis,
                        size = st_name_name_size,
                        font = st_name_name_font,
                    )
                else:
                    name = StudentName.objects.get(cardTable=card)
                    name.y_axis = st_name_y_axis
                    name.x_axis = st_name_x_axis
                    name.size = st_name_name_size
                    name.font = st_name_name_font
                    name.save()
    
            #grade
            if card.st_grade == True:
                st_grade_y_axis = request.POST['gradetop']
                st_grade_x_axis = request.POST['graderight']
                st_grade_name_size = request.POST['gradesize']
                st_grade_name_font = request.POST['gradefamily']
            
                if not StudentGrade.objects.filter(cardTable=card).exists():
                    StudentGrade.objects.create(
                        cardTable=card,
                        y_axis = st_grade_y_axis,
                        x_axis = st_grade_x_axis,
                        size = st_grade_name_size,
                        font = st_grade_name_font,
                    )
                else:
                    grade = StudentGrade.objects.get(cardTable=card)
                    grade.y_axis = st_grade_y_axis
                    grade.x_axis = st_grade_x_axis
                    grade.size = st_grade_name_size
                    grade.font = st_grade_name_font
                    grade.save()
            
            #icon
            if card.sc_icon == True:
                icon_width = request.POST['iconwidth']
                icon_height = request.POST['iconheight']
                icon_y_axis = request.POST['icontop']
                icon_x_axis = request.POST['iconright']
                icon_border = request.POST['iconborder']
                
                if not icon.objects.filter(cardTable=card).exists():
                    icon.objects.create(
                        cardTable=card,
                        width = icon_width,
                        height = icon_height,
                        y_axis = icon_y_axis,
                        x_axis = icon_x_axis,
                        border = icon_border,
                    )
                else:
                    icons = icon.objects.get(cardTable=card)
                    icons.width = icon_width
                    icons.height = icon_height
                    icons.y_axis = icon_y_axis
                    icons.x_axis = icon_x_axis
                    icons.border = icon_border
                    icons.save()
        
        if 'add' in request.POST:
            st_name = request.POST.get('st_name')
            if st_name == 'on':
                b = True
            else:
                b = False
            st_grade = request.POST.get('st_grade')
            if st_grade == 'on':
                c = True
            else:
                c = False
            sc_icon = request.POST.get('sc_icon')
            if sc_icon == 'on':
                d = True
            else:
                d = False
            table = request.POST.get('table')
            if table == 'on':
                g = True
            else:
                g = False
            card.table = g
            card.st_name = b
            card.st_grade = c
            card.sc_icon = d
            card.save()
        
        if 'textadd' in request.POST:
            a = request.POST['name']
            b = request.POST['text']
            line = request.POST.get('line')
            Text.objects.create(
                cardTable = card,
                name = a,
                text = b,
            )
              
        if 'textsave' in request.POST:
            a = request.POST['texttop']
            b = request.POST['textright']
            c = request.POST['textsize']
            d = request.POST['textfamily']
            id = request.POST['textid']
            te = Text.objects.get(pk=id)
            te.y_axis = a
            te.x_axis = b 
            te.size = c
            te.font = d
            te.save()
        
        if 'textdelete' in request.POST:
            id = request.POST['textid']
            te  = Text.objects.get(id=id)
            te.delete()
    
        if 'linesave' in request.POST:
            a = request.POST['linetop']
            b = request.POST['lineright']
            c = request.POST['linesize']
            id = request.POST['lineid']
            te = Line.objects.get(pk=id)
            te.y_axis = a
            te.x_axis = b 
            te.width = c
            te.save()
        
        if 'linedelete' in request.POST:
            id = request.POST['lineid']
            te  = Line.objects.get(id=id)
            te.delete()
    
        if 'makeline' in request.POST:
            c = Line.objects.filter(cardTable=card)
            d = Line.objects.create(name="1",cardTable=card) 
            d.name = d.id
            d.save()   
    
    
        return HttpResponseRedirect(request.path_info)
    alls = Profile.objects.filter(grade=student.profile.grade).count()
    year = AcademicYear.objects.last()
    context = {
                'web':web,
                'user':user,
                'name':name,
                'grade':grade,
                'student':student,
                'sub':sub,
                'tt':tt,
                'stat':stat,
                'card':card,
                'text':text,
                'line':line,
                'icon':ic,
                'alls':alls,
                'year':year,
            }
    return render(request,'teacher/card/add.html',context)




def design(request,id,id2,id3):
    web = Webpack.objects.get(pk=1)
    student = Student.objects.get(pk=id)
    profile = Profile.objects.get(id=student.profile.id)
    yyy = AcademicYear.objects.get(id=id3)
    sub = SubjectReslut.objects.filter(student=student,time=yyy)
    stat = StudentStatus.objects.get(student=student,time=yyy)
    card = cardType.objects.get(id=id2)
    site = get_current_site(request)
    u = request.user
    yes = 1
    alls = Profile.objects.filter(grade=student.profile.grade).count()
    times = History.objects.filter(user=student.profile.user)
    year = AcademicYear.objects.last()
    if u.is_authenticated:
        if Profile.objects.filter(user=u).exists():
            p = Profile.objects.get(user=u)
            if p.is_manager == True or p.is_teacher == True or p.is_staff == True:
                yes = 0
    text = Text.objects.filter(cardTable=card) .order_by("-id")
    line = Line.objects.filter(cardTable=card).order_by("-id")
    tt = 0
    name = 0
    grade = 0
    ic = 0
    if request.method == 'POST':
        if 'delete' in request.POST:
            card.delete()
            profile = Profile.objects.get(user=request.user.id)
            if Teacher.objects.filter(profile=profile).exists():
                teacher = Teacher.objects.get(profile=profile)
                return redirect("t_room" ,teacher.id)
        if 'generate' in request.POST:
            first = request.POST['one']
            second = request.POST['two']
            return redirect('t_dual' ,id=student.id,id2=card.id,first=first,second=second)
    
    if CTable.objects.filter(cardTable=card).exists():
        tt = CTable.objects.get(cardTable=card)
    if StudentName.objects.filter(cardTable=card).exists():
        name = StudentName.objects.get(cardTable=card)
    if StudentGrade.objects.filter(cardTable=card).exists():
        grade = StudentGrade.objects.get(cardTable=card)
    if icon.objects.filter(cardTable=card).exists():
        ic = icon.objects.get(cardTable=card)
    context = {
                'web':web,
                'name':name,
                'grade':grade,
                'student':student,
                'sub':sub,
                'tt':tt,
                'stat':stat,
                'card':card,
                'text':text,
                'line':line,
                'yes':yes,
                'icon':ic,
                'site':site,
                'times':times,'alls':alls,
                'year':year,
            }
    return render(request,'teacher/card/design.html',context)




def dual(request,id,id2,first,second):
        if 'generate' in request.POST:
            first = request.POST['one']
            second = request.POST['two']
            return redirect('t_dual' ,id=student.id,id2=card.id,first=first,second=second)
        if first == 'current' and second != 'current':
                noo=2
                web = Webpack.objects.get(pk=1)
                student = Student.objects.get(pk=id)
                profile = Profile.objects.get(id=student.profile.id)
                sub = SubjectReslut.objects.filter(student=student,time=student.year)
                stat = StudentStatus.objects.get(student=student,time=student.year)
                card = cardType.objects.get(id=id2)
                site = get_current_site(request)
                times = History.objects.filter(user=student.profile.user)
                u = request.user
                yes = 1
                alls = Profile.objects.filter(grade=student.profile.grade).count()


                second = History.objects.get(id=second)
                subs = SubjectReslutHistory.objects.filter(student=second)
                stats = StudentStatusHistory.objects.get(student=second)
                if u.is_authenticated:
                    if Profile.objects.filter(user=u).exists():
                        p = Profile.objects.get(user=u)
                        if p.is_manager == True or p.is_teacher == True or p.is_staff == True:
                            yes = 0
                text = Text.objects.filter(cardTable=card) .order_by("-id")
                line = Line.objects.filter(cardTable=card).order_by("-id")
                tt = 0
                name = 0
                grade = 0
                ic = 0
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        card.delete()
                        profile = Profile.objects.get(user=request.user.id)
                        if Teacher.objects.filter(profile=profile).exists():
                            teacher = Teacher.objects.get(profile=profile)
                            return redirect("t_room" ,teacher.id)

                if CTable.objects.filter(cardTable=card).exists():
                    tt = CTable.objects.get(cardTable=card)
                if StudentName.objects.filter(cardTable=card).exists():
                    name = StudentName.objects.get(cardTable=card)
                if StudentGrade.objects.filter(cardTable=card).exists():
                    grade = StudentGrade.objects.get(cardTable=card)
                if icon.objects.filter(cardTable=card).exists():
                    ic = icon.objects.get(cardTable=card)
                context = {
                            'web':web,
                            'name':name,
                            'grade':grade,
                            'student':student,
                            'sub':sub,
                            'tt':tt,
                            'stat':stat,
                            'second':second,
                            'subs':subs,
                            'stats':stats,
                            'card':card,
                            'times':times,
                            'text':text,
                            'line':line,
                            'yes':yes,
                            'icon':ic,
                            'site':site,
                            'noo':noo,
                            'alls':alls,
                        }
                return render(request,'teacher/card/dual.html',context)
        if second == 'current' and first != 'current':
                noo = 1
                web = Webpack.objects.get(pk=1)
                student = Student.objects.get(pk=id)
                profile = Profile.objects.get(id=student.profile.id)
                sub = SubjectReslut.objects.filter(student=student,time=student.year)
                stat = StudentStatus.objects.get(student=student,time=student.year)
                card = cardType.objects.get(id=id2)
                site = get_current_site(request)
                times = History.objects.filter(user=student.profile.user)
                u = request.user
                yes = 1
                alls = Profile.objects.filter(grade=student.profile.grade).count()


                second = History.objects.get(id=first)
                subs = SubjectReslutHistory.objects.filter(student=first)
                stats = StudentStatusHistory.objects.get(student=first)
                if u.is_authenticated:
                    if Profile.objects.filter(user=u).exists():
                        p = Profile.objects.get(user=u)
                        if p.is_manager == True or p.is_teacher == True or p.is_staff == True:
                            yes = 0
                text = Text.objects.filter(cardTable=card) .order_by("-id")
                line = Line.objects.filter(cardTable=card).order_by("-id")
                tt = 0
                name = 0
                grade = 0
                ic = 0
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        card.delete()
                        profile = Profile.objects.get(user=request.user.id)
                        if Teacher.objects.filter(profile=profile).exists():
                            teacher = Teacher.objects.get(profile=profile)
                            return redirect("t_room" ,teacher.id)

                if CTable.objects.filter(cardTable=card).exists():
                    tt = CTable.objects.get(cardTable=card)
                if StudentName.objects.filter(cardTable=card).exists():
                    name = StudentName.objects.get(cardTable=card)
                if StudentGrade.objects.filter(cardTable=card).exists():
                    grade = StudentGrade.objects.get(cardTable=card)
                if icon.objects.filter(cardTable=card).exists():
                    ic = icon.objects.get(cardTable=card)
                context = {
                            'web':web,
                            'name':name,
                            'grade':grade,
                            'student':student,
                            'sub':sub,
                            'tt':tt,
                            'stat':stat,
                            'second':second,
                            'subs':subs,
                            'stats':stats,
                            'card':card,
                            'times':times,
                            'text':text,
                            'line':line,
                            'yes':yes,
                            'icon':ic,
                            'noo':noo,
                            'site':site,
                            'alls':alls,
                        }
                return render(request,'teacher/card/dual.html',context)
        if second == 'current' and first == 'current':
                noo = 3
                web = Webpack.objects.get(pk=1)
                student = Student.objects.get(pk=id)
                profile = Profile.objects.get(id=student.profile.id)
                sub = SubjectReslut.objects.filter(student=student,time=student.year)
                stat = StudentStatus.objects.get(student=student,time=student.year)
                card = cardType.objects.get(id=id2)
                site = get_current_site(request)
                times = History.objects.filter(user=student.profile.user)
                u = request.user
                yes = 1
                alls = Profile.objects.filter(grade=student.profile.grade).count()


                
                if u.is_authenticated:
                    if Profile.objects.filter(user=u).exists():
                        p = Profile.objects.get(user=u)
                        if p.is_manager == True or p.is_teacher == True or p.is_staff == True:
                            yes = 0
                text = Text.objects.filter(cardTable=card) .order_by("-id")
                line = Line.objects.filter(cardTable=card).order_by("-id")
                tt = 0
                name = 0
                grade = 0
                ic = 0
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        card.delete()
                        profile = Profile.objects.get(user=request.user.id)
                        if Teacher.objects.filter(profile=profile).exists():
                            teacher = Teacher.objects.get(profile=profile)
                        if Staff.objects.filter(profile=profile).exists():
                            teacher = Staff.objects.get(profile=profile)
                            return redirect("t_room" ,teacher.id)

                if CTable.objects.filter(cardTable=card).exists():
                    tt = CTable.objects.get(cardTable=card)
                if StudentName.objects.filter(cardTable=card).exists():
                    name = StudentName.objects.get(cardTable=card)
                if StudentGrade.objects.filter(cardTable=card).exists():
                    grade = StudentGrade.objects.get(cardTable=card)
                if icon.objects.filter(cardTable=card).exists():
                    ic = icon.objects.get(cardTable=card)
                context = {
                            'web':web,
                            'name':name,
                            'grade':grade,
                            'student':student,
                            'sub':sub,
                            'tt':tt,
                            'stat':stat,
                            'card':card,
                            'times':times,
                            'text':text,
                            'line':line,
                            'yes':yes,
                            'icon':ic,
                            'noo':noo,
                            'site':site,
                            'alls':alls,
                        }
                return render(request,'teacher/card/dual.html',context)
        if first != 'current' and second != 'current':
                noo=4
                web = Webpack.objects.get(pk=1)
                student = Student.objects.get(pk=id)
                profile = Profile.objects.get(id=student.profile.id)
                sub = SubjectReslut.objects.filter(student=student,time=student.year)
                stat = StudentStatus.objects.get(student=student,time=student.year)
                card = cardType.objects.get(id=id2)
                site = get_current_site(request)
                times = History.objects.filter(user=student.profile.user)
                u = request.user
                yes = 1
                alls = Profile.objects.filter(grade=student.profile.grade).count()


                second = History.objects.get(id=second)
                subs = SubjectReslutHistory.objects.filter(student=second)
                stats = StudentStatusHistory.objects.get(student=second)
                if u.is_authenticated:
                    if Profile.objects.filter(user=u).exists():
                        p = Profile.objects.get(user=u)
                        if p.is_manager == True or p.is_teacher == True or p.is_staff == True:
                            yes = 0
                text = Text.objects.filter(cardTable=card) .order_by("-id")
                line = Line.objects.filter(cardTable=card).order_by("-id")
                tt = 0
                name = 0
                grade = 0
                ic = 0
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        card.delete()
                        profile = Profile.objects.get(user=request.user.id)
                        if Teacher.objects.filter(profile=profile).exists():
                            teacher = Teacher.objects.get(profile=profile)
                            return redirect("t_room" ,teacher.id)

                if CTable.objects.filter(cardTable=card).exists():
                    tt = CTable.objects.get(cardTable=card)
                if StudentName.objects.filter(cardTable=card).exists():
                    name = StudentName.objects.get(cardTable=card)
                if StudentGrade.objects.filter(cardTable=card).exists():
                    grade = StudentGrade.objects.get(cardTable=card)
                if icon.objects.filter(cardTable=card).exists():
                    ic = icon.objects.get(cardTable=card)
                context = {
                            'web':web,
                            'name':name,
                            'grade':grade,
                            'student':student,
                            'sub':sub,
                            'tt':tt,
                            'stat':stat,
                            'second':second,
                            'subs':subs,
                            'stats':stats,
                            'card':card,
                            'times':times,
                            'text':text,
                            'line':line,
                            'yes':yes,
                            'icon':ic,
                            'site':site,
                            'noo':noo,
                            'alls':alls,
                        }
                return render(request,'teacher/card/dual.html',context)