from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from home.models import *
from .models import *
from redirector.models import *
from teacher.models import Teacher,Subject, GradePost
from manager.models import StudentMessage
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
#from rank import DenseRank, UpperRank, Rank
from django.contrib.sites.shortcuts import get_current_site


@login_required(login_url='login')
def year(request):
    event = Event.objects.all()
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    year = AcademicYear.objects.last()
    history = History.objects.filter(user=user)
    context = {
        'event':event,
        "web":web,
        'user':user,
        'student':student,
        'year':year,
        'history':history,
    }
    return render(request,'student/year.html',context)

@login_required(login_url='login')
def year_history(request,year,username):
    event = Event.objects.all()
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    u = User.objects.get(username=username)
    y = AcademicYear.objects.get(year=year)
    history = History.objects.get(academicYear=y,user=u)
    link = History.objects.filter(user=user)
    test = TestHistory.objects.filter(history=history)
    result = ResultHistory.objects.filter(student=student)
    subject = Subject.objects.filter(grade=pp.grade)
    average = "0"
    total = test.aggregate(Sum('capacity'))['capacity__sum']
    alltotal = result.aggregate(Sum('status'))['status__sum']
    if not total:
        total='0'
    allfrom = total * subject.count()
    if result:
        if allfrom != 0:
            average = (alltotal/allfrom)*100
        else:
            allfrom=1
            average = (alltotal/allfrom)*100
    context = {
        'event':event,
        'test':test,
        'subject':subject,
        'result':result,
        'total':total,
        'alltotal':alltotal,
        'allfrom':allfrom,
        'average':average,
        "web":web,
        'result':result,
        'user':user,
        'student':student,
        'year':year,
        'student':student,
        'history':history,
        'link':link,
    }
    return render(request,'student/year-history.html',context)

@login_required(login_url='login')
def index(request):
    event = Event.objects.all()
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    total_grade = Profile.objects.filter(grade=pp.grade,is_student=True).count()
    if StudentStatus.objects.filter(student=student).exists():
        st = StudentStatus.objects.get(student=student)
    else:
        st = StudentStatus.objects.create(student=student,first_total=0,first_from=0,first_average=0,second_total=0,second_from=0,second_average=0,time=student.year)
    mmm = StudentMessage.objects.all().count()
    if mmm>2:
        manager_message = StudentMessage.objects.all()[(mmm-2):mmm]
    else:
        manager_message = StudentMessage.objects.all()[:mmm]
    grade_post = GradePost.objects.filter(for_grade=pp.grade).order_by("-id")
    students = Profile.objects.filter(grade=pp.grade)
    test = Test.objects.filter(grade=pp.grade)
    result = Result.objects.filter(student=student)
    subject = Subject.objects.filter(grade=pp.grade)
    average = "0"
    if result:
        total = test.aggregate(Sum('capacity'))['capacity__sum']
        alltotal = result.aggregate(Sum('status'))['status__sum']
        allfrom = total * subject.count()
        average = (alltotal/allfrom)*100
    context = {
        'event':event,
        "web":web,
        'average':average,
        'user':user,
        'student':student,
        'st':st,
        'total_grade':total_grade,
        'manager_message':manager_message,
        'grade_post':grade_post,
        'students':students,
    }
    return render(request,'student/index.html',context)

@login_required(login_url='login')
def searchStudent(request):
    event = Event.objects.all()
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    chats = Chat.objects.filter(grade=pp.grade)
    if request.method == 'POST':
        if 'sendsearch' in request.POST:
            search = request.POST['searched']
            chat_student = Student.objects.filter(first_name__icontains=search)
            s = search
    context = {
        "web":web,
        'user':user,
        'event':event,
        'student':student,
        'chat':chat_student,
        's':s,
        'chats':chats,
    }
    return render(request,'student/search.html',context)

@login_required(login_url='login')
def chatting(request):
    event = Event.objects.all()
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    chat_student = Student.objects.all().exclude(profile=pp)
    chats = Chat.objects.filter(grade=pp.grade)
    if request.method == "POST":
        if 'sendchat' in request.POST:
            a = request.POST['chat']
            Chat.objects.create(message=a,grade=pp.grade,sender=student)
    context = {
        "web":web,
        'user':user,
        'student':student,
        'chat':chat_student,
        'chats':chats,
        'event':event,
    }
    return render(request,'student/chat.html',context)


@login_required(login_url='login')
def users(request,username):
    web = Webpack.objects.get(pk=1)
    user = request.user
    event = Event.objects.all()
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    b = User.objects.get(username=username)
    c = Profile.objects.get(user=b)
    d = Student.objects.get(profile=c)
    chat_student = Student.objects.all().exclude(profile=c)
    chats = Chat.objects.filter(grade=pp.grade)
    if request.method == "POST":
        if 'sendchat' in request.POST:
            a = request.POST['chat']
            Chat.objects.create(message=a,grade=pp.grade,sender=student)
    context = {
        "web":web,
        'user':user,
        'student':student,
        'chat':chat_student,
        'event':event,
        'chats':chats,
        'd':d
    }
    return render(request,'student/users.html',context)


@login_required(login_url='login')
def Books(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    event = Event.objects.all()
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    lib = Library.objects.filter(for_student=True)
    context = {
        "web":web,
        'event':event,
        'user':user,
        'student':student,
        'lib':lib
    }
    return render(request,'student/library.html',context)


@login_required(login_url='login')
def Courses(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    event = Event.objects.all()
    student = Student.objects.get(profile=pp)
    teacher = Teacher.objects.all()
    sub = Subject.objects.all()
    course = Course.objects.all()
    context = {
        "web":web,
        'event':event,
        'user':user,
        'student':student,
        'teacher':teacher,
        'sub':sub,
        'course':course,
    }
    return render(request,'student/course/index.html',context)

@login_required(login_url='login')
def subject(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    event = Event.objects.all()
    teacher = Teacher.objects.all()
    sub = Subject.objects.all()
    course = Course.objects.filter(subject=id)
    context = {
        "web":web,
        'user':user,
        'student':student,
        'teacher':teacher,
        'event':event,
        'sub':sub,
        'course':course,
    }
    return render(request,'student/course/subject.html',context)



@login_required(login_url='login')
def result(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    if StudentStatus.objects.filter(student=student,time=student.year).exists():
        stat = StudentStatus.objects.get(student=student,time=student.year)
        substat = SubjectReslut.objects.filter(student=student,time=student.year)
    else:
        stat = None
        substat = None
    teacher = Teacher.objects.all()
    event = Event.objects.all()
    sub = Subject.objects.all()
    test = Test.objects.filter(grade=pp.grade,time="first academic term",year=AcademicYear.objects.last())
    result = Result.objects.filter(student=student,time="first academic term",year=AcademicYear.objects.last())
    subject = Subject.objects.filter(grade=pp.grade).order_by('name')
    average = "0"
    site = get_current_site(request)
    total = test.aggregate(Sum('capacity'))['capacity__sum']
    alltotal=0
    allfrom=0
    try:
        if result:
            alltotal = result.aggregate(Sum('status'))['status__sum']
            allfrom = total * subject.count()
            if result:
                if allfrom != 0:
                    average = (alltotal/allfrom)*100
                else:
                    allfrom=1
                    average = (alltotal/allfrom)*100
                if average <50:
                    messages.error(request,"You are failed please study hard! your first academic term average is  less than the half")
    except:return redirect("r_index")
    testtwo = Test.objects.filter(grade=pp.grade,time="second academic term",year=AcademicYear.objects.last())
    resulttwo = Result.objects.filter(student=student,time="second academic term",year=AcademicYear.objects.last())
    subjecttwo = Subject.objects.filter(grade=pp.grade)
    averagetwo = "0"
    totaltwo = testtwo.aggregate(Sum('capacity'))['capacity__sum']
    alltotaltwo=0
    allfromtwo=0
    if resulttwo:
        alltotaltwo = resulttwo.aggregate(Sum('status'))['status__sum']
        allfromtwo = totaltwo * subjecttwo.count()
        if resulttwo:
            averagetwo = (alltotaltwo/allfromtwo)*100
            if averagetwo <50:
                messages.error(request,"You are failed please study hard! your second academic term average is  less than the half")
    subjects = Subject.objects.filter(grade=student.profile.grade)
    tests = Test.objects.filter(year=student.year,grade=student.profile.grade )
    results = Result.objects.filter(year=student.year,student=student)
    if SubjectReslut.objects.filter(student=student,time=student.year,grade=student.profile.grade).exists():
        stat = SubjectReslut.objects.filter(student=student,time=student.year,grade=student.profile.grade)
    else:
        stat = None
    if StudentStatus.objects.filter(student=student,time=student.year).exists():
        i = StudentStatus.objects.get(student=student,time=student.year)
    else:
        i=None
    context = {
        'subjects':subjects,
        'stat':stat,
        'i':i,
        'tests':tests,
        'results':results,
        "web":web,
        'user':user,
        'student':student,
        'teacher':teacher,
        'event':event,
        'sub':sub,
        'site':site,
        'test':test,
        'subject':subject,
        'result':result,
        'total':total,
        'alltotal':alltotal,
        'allfrom':allfrom,
        'average':average,
        'testtwo':testtwo,
        'subjecttwo':subjecttwo,
        'resulttwo':resulttwo,
        'totaltwo':totaltwo,
        'alltotaltwo':alltotaltwo,
        'allfromtwo':allfromtwo,
        'averagetwo':averagetwo,
        'stat':stat,
        'substat':substat,
    }
    return render(request,'student/result.html',context)


@login_required(login_url='login')
def Historyresult(request,year):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    st = Student.objects.get(profile=pp)
    y = AcademicYear.objects.get(year=year)
    student = History.objects.get(user=user,academicYear=y)
    stat = StudentStatusHistory.objects.get(student=student,time=y)
    substat = SubjectReslutHistory.objects.filter(student=student,time=y)
    teacher = Teacher.objects.all()
    event = Event.objects.all()
    sub = Subject.objects.all()
    test = TestHistory.objects.filter(time="first academic term",academicYear=y)
    result = ResultHistory.objects.filter(student=st,time="first academic term",year=y)
    subject = Subject.objects.filter(grade=pp.grade)
    average = "0"
    site = get_current_site(request)
    total = test.aggregate(Sum('capacity'))['capacity__sum']
    alltotal=0
    allfrom=0
    if result:
        alltotal = result.aggregate(Sum('status'))['status__sum']
        allfrom = total * subject.count()
        if result:
            average = (alltotal/allfrom)*100
            if average <50:
                messages.error(request,"You are failed please study hard! your first academic term average is  less than the half")
    testtwo = Test.objects.filter(grade=pp.grade,time="second academic term",year=y)
    resulttwo = Result.objects.filter(student=st,time="second academic term",year=y)
    subjecttwo = Subject.objects.filter(grade=pp.grade)
    averagetwo = "0"
    totaltwo = testtwo.aggregate(Sum('capacity'))['capacity__sum']
    alltotaltwo=0
    allfromtwo=0
    if resulttwo:
        alltotaltwo = resulttwo.aggregate(Sum('status'))['status__sum']
        allfromtwo = totaltwo * subjecttwo.count()
        if resulttwo:
            averagetwo = (alltotaltwo/allfromtwo)*100
            if averagetwo <50:
                messages.error(request,"You are failed please study hard! your second academic term average is  less than the half")
    context = {
        "web":web,
        'user':user,
        'student':student,
        'teacher':teacher,
        'event':event,
        'sub':sub,
        'site':site,
        'test':test,
        'subject':subject,
        'result':result,
        'total':total,
        'alltotal':alltotal,
        'allfrom':allfrom,
        'average':average,
        'testtwo':testtwo,
        'subjecttwo':subjecttwo,
        'resulttwo':resulttwo,
        'totaltwo':totaltwo,
        'alltotaltwo':alltotaltwo,
        'allfromtwo':allfromtwo,
        'averagetwo':averagetwo,
        'stat':stat,
        'substat':substat,
        'st':st,
        'y':y,
    }
    return render(request,'student/history/history.html',context)


@login_required(login_url='login')
def his(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    event = Event.objects.all()
    his = History.objects.filter(user=user)
    context = {
        "web":web,
        'user':user,
        'event':event,
        'student':student,
        'his':his,
    }
    return render(request,'student/history/main.html',context)
    


@login_required(login_url='login')
def page(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    teacher = Teacher.objects.all()
    event = Event.objects.all()
    sub = Subject.objects.all()
    course = Course.objects.get(id=id)
    a = course.views
    b = a+1
    course.views=b
    course.save()
    yes = Teacher.objects.filter(subscribers=pp).exists()
    c = CourseComment.objects.filter(course=id)
    cc = Course.objects.all().exclude(id=id)
    if request.method == 'POST':
        if 'subscribe' in request.POST:
            a = Teacher.objects.get(id=course.posted_by.id)
            a.subscribers.add(pp)
            a.save()
            messages.success(request,'subscribed succesfully')
            return redirect('page' ,course.id)
        if 'unsubscribe' in request.POST:
            a = Teacher.objects.get(id=course.posted_by.id)
            a.subscribers.remove(pp)
            a.save()
            messages.success(request,'subscribtion removed succesfully')
            return redirect('page' ,course.id)
        if 'comment' in request.POST:
            a = request.POST['message']
            CourseComment.objects.create(course=course,message=a,sender=student)
            messages.success(request,'comment posted succesfully')
    context = {
        "web":web,
        'event':event,
        'user':user,
        'student':student,
        'teacher':teacher,
        'sub':sub,
        'course':course,
        'yes':yes,
        'c':c,
        'cc':cc,
    }
    return render(request,'student/course/page.html',context)


@login_required(login_url='login')
def Coursesearch(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    event = Event.objects.all()
    student = Student.objects.get(profile=pp)
    teacher = Teacher.objects.all()
    if request.method == 'POST':
        a = request.POST.get('searched')
        courses = Course.objects.filter(name__icontains=a)
    context = {
        "web":web,
        'user':user,
        'event':event,
        'student':student,
        'teacher':teacher,
        'course':courses,
        'a':a,
    }
    return render(request,'student/course/search.html',context)


@login_required(login_url='login')
def teacher(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    teacher = Teacher.objects.get(id=id)
    event = Event.objects.all()
    yes = Teacher.objects.filter(subscribers=pp)
    courses = Course.objects.filter(posted_by=teacher.id)
    a = ''
    if request.method == 'POST':
        if 'searchsubmit' in request.POST:
            a = request.POST['tsearch']
            courses = Course.objects.filter(posted_by=teacher.id).filter(name__icontains=a)
        if 'subscribe' in request.POST:
            teacher.subscribers.add(pp)
            teacher.save()
            messages.success(request,'subscribed succesfully')
        if 'unsubscribe' in request.POST:
            teacher.subscribers.remove(pp)
            teacher.save()
            messages.success(request,'subscribtion removed succesfully')
    context = {
        "web":web,
        'user':user,
        'student':student,
        'teacher':teacher,
        'yes':yes,
        'event':event,
        'course':courses,
        'a':a,
    }
    return render(request,'student/course/teacher.html',context)


@login_required(login_url='login')
def teachermessage(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    teacher = Teacher.objects.get(id=id)
    yes = Teacher.objects.filter(subscribers=pp)
    event = Event.objects.all()
    courses = Course.objects.filter(posted_by=teacher.id)
    a = ''
    grade_post = GradePost.objects.filter(for_grade=pp.grade,teacher=teacher.id)
    if request.method == 'POST':
        if 'searchsubmit' in request.POST:
            a = request.POST['tsearch']
            courses = Course.objects.filter(posted_by=teacher.id).filter(name__icontains=a)
        if 'subscribe' in request.POST:
            teacher.subscribers.add(pp)
            teacher.save()
            messages.success(request,'subscribed succesfully')
        if 'unsubscribe' in request.POST:
            teacher.subscribers.remove(pp)
            teacher.save()
            messages.success(request,'subscribtion removed succesfully')
    context = {
        "web":web,
        'user':user,
        'student':student,
        'teacher':teacher,
        'yes':yes,
        'course':courses,
        'event':event,
        'a':a,
        'grade':grade_post,
    }
    return render(request,'student/course/tmessage.html',context)


@login_required(login_url='login')
def teacherbook(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    event = Event.objects.all()
    student = Student.objects.get(profile=pp)
    teacher = Teacher.objects.get(id=id)
    yes = Teacher.objects.filter(subscribers=pp)
    courses = Course.objects.filter(posted_by=teacher.id)
    a = ''
    lib = Library.objects.filter(for_student=True,posted_by=teacher.profile)
    if request.method == 'POST':
        if 'searchsubmit' in request.POST:
            a = request.POST['tsearch']
            courses = Course.objects.filter(posted_by=teacher.id).filter(name__icontains=a)
        if 'subscribe' in request.POST:
            teacher.subscribers.add(pp)
            teacher.save()
            messages.success(request,'subscribed succesfully')
        if 'unsubscribe' in request.POST:
            teacher.subscribers.remove(pp)
            teacher.save()
            messages.success(request,'subscribtion removed succesfully')
    context = {
        "web":web,
        'user':user,
        'student':student,
        'teacher':teacher,
        'yes':yes,
        'course':courses,
        'a':a,
        'lib':lib,
        'event':event,
    }
    return render(request,'student/course/tbook.html',context)




@login_required(login_url='login')
def getChat(request,username):
    a = User.objects.get(username=username)
    pp = Profile.objects.get(user=a)
    messages = Chat.objects.filter(grade=pp.grade)
    return JsonResponse({"messages":list(messages.values())})



@login_required(login_url='login')
def StudentProfile(request):
    web = Webpack.objects.get(pk=1)
    me = request.user
    event = Event.objects.all()
    pp = Profile.objects.get(user=me)
    student = Student.objects.get(profile=pp)
    if request.method == 'POST':
        try:
            if 'update' in request.POST:
                first_name = request.POST['firstName']
                last_name = request.POST['lastName']
                email = request.POST['email']
                username = request.POST['username']
                phone = request.POST['phone']
                address = request.POST['address']
                birth = request.POST['birth']
                p1 = request.POST['password1']
                p2 = request.POST['password2']
                nationality = request.POST['nationality']
                p = Password.objects.get(of=me)
                if request.FILES:
                    profile_pic = request.FILES['profile_pic']
                    student.profile_pic = profile_pic
                    student.save()
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
                            student.username=username
                            student.save()
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
                        student.first_name = first_name
                        student.last_name = last_name
                        student.save()
                        messages.success("Your name is updated successfully")
                if email:
                    if not User.objects.filter(email=email).exists():
                        me.email = email
                        p.email = email
                        me.save()
                        p.save()
                        messages.success("Email Updated Successfully")
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
                if address:
                    if not Student.objects.filter(city=address).exists():
                        student.city=address
                        student.save()
                        messages.success(request,"Current City updated Successfully!")
                if birth:
                    student.birth=birth
                    student.save()
                    messages.success(request,'Your Birthday is updated Successfully!')
                if nationality:
                    if not Student.objects.filter(nationality=nationality).exists():
                        student.nationality=nationality
                        student.save()
                        messages.success(request,"The change in your nationality is saved successfully!")
            if 'delete' in request.POST:
                me.delete()
                messages.success(request,"Hey Dear user glad to work with you thank you for everything good bye!")
                return redirect('r_index')
        except:pass
    context = {
        "web":web,
        'event':event,
        'user':me,
        'student':student,
    }
    return render(request,'student/profile.html',context)


@login_required(login_url='login')
def waiting(request):
    user=request.user
    pp = Profile.objects.get(user=user)
    student = Student.objects.get(profile=pp)
    if student.is_verified:
        return redirect("s_index")
    else:
        return render(request,'student/waiting.html',{'user':user})


@login_required(login_url='login')
def deleteaccount(request,id):
    user=User.objects.get(pk=id)
    user.delete()
    return redirect("r_index")