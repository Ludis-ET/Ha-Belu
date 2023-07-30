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
from manager.models import Manager
from django.contrib import messages
from teacher.models import *
from django.db.models import Sum
from teacher.models import *
from teacher.views import save_student_history
from manager.views import laststudent

@login_required(login_url='login')
def index(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    staff = Staff.objects.get(profile=pp)
    managers = None
    teachers = None
    students = None
    staffes = None
    today = AcademicYear.objects.last()
    next = today.year + 1
    if staff.verify_user == True:
        managers = Manager.objects.filter(is_verified=False)
        teachers = Teacher.objects.filter(is_verified=False)
        students = Student.objects.filter(is_verified=False)
        staffes = Staff.objects.filter(is_verified=False)
        if request.method == 'POST':
            if 'accept' in request.POST:
                items = request.POST.getlist('check')
                for a in items:
                    u = User.objects.get(id=a)
                    p = Profile.objects.get(user=u)
                    if Manager.objects.filter(profile=p).exists():
                        m = Manager.objects.get(profile=p)
                        m.is_verified = True
                        m.save()
                        messages.success(request,'accepted successfully!')
                        return redirect('r_index')
                    elif Teacher.objects.filter(profile=p).exists():
                        m = Teacher.objects.get(profile=p)
                        m.is_verified = True
                        m.save()
                        messages.success(request,'accepted successfully!')
                        return redirect('r_index')
                    elif Student.objects.filter(profile=p).exists():
                        m = Student.objects.get(profile=p)
                        m.is_verified = True
                        m.save()
                        messages.success(request,'accepted successfully!')
                        return redirect('r_index')
                    elif Staff.objects.filter(profile=p).exists():
                        m = Staff.objects.get(profile=p)
                        m.is_verified = True
                        m.save()
                        messages.success(request,'accepted successfully!')
                        return redirect('r_index')
                    else:
                        messages.error(request,'user not found')
                        return redirect('r_index')
            if 'reject' in request.POST:
                items = request.POST.getlist('check')
                for a in items:
                    u = User.objects.get(id=a)
                    u.delete()
                    messages.success(request,'user deleted!')
                    return redirect('r_index')
    
    if staff.time == True:
        if request.method == 'POST':
            if 'yes' in request.POST:
                AcademicYear.objects.create(year=next,new=True)
                messages.success(request,'Academic year changed successfully now you have to transfer students to this year')
                return redirect('r_index')
            if 'transfer' in request.POST:
                aaa = AcademicYear.objects.last()
                aaa.new = False
                aaa.save()
                return redirect('m_transfer')
            
    context = {
        "web":web,
        'user':user,
        'staff':staff,
        'managers':managers,
        'teachers':teachers,
        'students':students,
        'staffes':staffes,
        'today':today,
        'next':next,
    }
    return render(request,'staff/index.html',context)


@login_required(login_url='login')
def result(request):
    grades = Grade.objects.all()
            
    context = {
        "grades":grades,
    }
    return render(request,'staff/result.html',context)



@login_required(login_url='login')
def grade_result(request,id):
    grade = Grade.objects.get(id=id)
    grades = Grade.objects.all()
    year = AcademicYear.objects.last()
    tag = 'green'
    tests = Test.objects.filter(year=year,grade=grade)
    students = Student.objects.filter(grade=grade.name).order_by("first_name",'last_name')
    if request.method == 'POST':
        try:
            semester = request.POST['semester']
            
            if semester == 'First Academic Year':
                t = request.POST['test']
                test = Test.objects.get(time='first academic term',name=t)
                s = request.POST['subject']
                semester = 'first academic term'
                subject = Subject.objects.get(name=s)
                for ss in students:
                    capacity = request.POST[ss.username]
                    if Result.objects.filter(name=test,subject=subject,time=semester,student=ss,year=year).exists():
                        result = Result.objects.get(name=test,subject=subject,time=semester,student=ss,year=year)
                        result.status = capacity
                        result.save()
                    else:
                        Result.objects.create(name=test,subject=subject,time=semester,student=ss,year=year,status=capacity)

                    all_total = Result.objects.filter(student=ss,time="first academic term",year=AcademicYear.objects.last()).aggregate(Sum('status'))['status__sum']
                    total = Result.objects.filter(student=ss,time="first academic term",year=AcademicYear.objects.last(),subject=subject).aggregate(Sum('status'))['status__sum']
                    test_total = Test.objects.filter(grade=ss.profile.grade,subject=subject,time="first academic term",year=year).aggregate(Sum('capacity'))['capacity__sum']
                    if SubjectReslut.objects.filter(subject=subject,grade=ss.profile.grade,student=ss,time=year).exists():
                        result = SubjectReslut.objects.get(subject=subject,grade=ss.profile.grade,student=ss,time=year)
                        result.first = total
                        result.f_from = test_total
                        result.save()
                    else:
                        SubjectReslut.objects.create(subject=subject,grade=ss.profile.grade,student=ss,time=year,first=total,f_from=test_total)


                    if test_total:
                        tot = (test_total * Subject.objects.filter(grade=ss.profile.grade).count())
                        if tot != 0 :
                            average = (all_total/tot)*100
                        else:
                            average = (0/1)*100
                    else:
                        tot = 0
                        average = (all_total/1)*100
                    ss.average = average
                    ss.save()

                    if StudentStatus.objects.filter(student=ss,time=year).exists():
                        aaaa = StudentStatus.objects.get(student=ss,time=year)
                        aaaa.first_average=average
                        aaaa.first_from=tot
                        aaaa.first_total=all_total
                        aaaa.grade=ss.profile.grade
                        if aaaa.first_total and aaaa.second_total:
                            aaaa.average=((aaaa.first_total+aaaa.second_total)/(aaaa.first_from+aaaa.second_from))*100
                        else:
                            average=0
                        aaaa.save()
                    else:
                        StudentStatus.objects.create(student=ss,time=year,first_average=average,first_from=tot,first_total=total)



            elif semester == 'Second Academic Year':
                t = request.POST['test']
                test = Test.objects.get(time='second academic term',name=t)
                s = request.POST['subject']
                semester = 'second academic term'
                subject = Subject.objects.get(name=s)
                for ss in students:
                    capacity = request.POST[ss.username]
                    if Result.objects.filter(name=test,subject=subject,time=semester,student=ss,year=year).exists():
                        result = Result.objects.get(name=test,subject=subject,time=semester,student=ss,year=year)
                        result.status = capacity
                        result.save()
                    else:
                        Result.objects.create(name=test,subject=subject,time=semester,student=ss,year=year,status=capacity)


                    all_total = Result.objects.filter(student=ss,time="second academic term",year=AcademicYear.objects.last()).aggregate(Sum('status'))['status__sum']
                    total = Result.objects.filter(student=ss,time="second academic term",year=AcademicYear.objects.last(),subject=subject).aggregate(Sum('status'))['status__sum']
                    test_total = Test.objects.filter(grade=ss.profile.grade,subject=subject,time="second academic term",year=year).aggregate(Sum('capacity'))['capacity__sum']
                    if SubjectReslut.objects.filter(subject=subject,grade=ss.profile.grade,student=ss,time=year).exists():
                        result = SubjectReslut.objects.get(subject=subject,grade=ss.profile.grade,student=ss,time=year)
                        result.second = total
                        result.s_from = test_total
                        if result.first is not None and result.second is not None:
                            result.year = result.first + result.second
                        result.save()
                    else:
                        SubjectReslut.objects.create(subject=subject,grade=ss.profile.grade,student=ss,time=year,second=total,s_from=test_total)


                    if test_total:
                        tot = (test_total * Subject.objects.filter(grade=ss.profile.grade).count())
                        if tot != 0 :
                            average = (all_total/tot)*100
                        else:
                            average = (0/1)*100
                    else:
                        tot = 0
                        average = (all_total/1)*100
                    ss.average = average
                    ss.save()

                    if StudentStatus.objects.filter(student=ss,time=year).exists():
                        aaaa = StudentStatus.objects.get(student=ss,time=year)
                        aaaa.second_average=average
                        aaaa.second_from=tot
                        aaaa.second_total=all_total
                        aaaa.grade=ss.profile.grade
                        if aaaa.first_total and aaaa.second_total:
                            aaaa.total = (aaaa.first_total + aaaa.second_total)
                            aaaa.average=((aaaa.first_total+aaaa.second_total)/(aaaa.first_from+aaaa.second_from))*100
                        else:
                            average=0
                        aaaa.save()
                    else:
                        StudentStatus.objects.create(student=ss,time=year,first_average=average,second_from=tot,second_total=total)
            tag = 'green'
            messages.success(request,'Result posted successfully!')
            return redirect('st_grade_result',grade.id)
        except:
            tag = 'red'
            messages.error(request,'Please Try Again')
            return redirect('st_grade_result',grade.id)
    context = {
        "grades":grades,
        'tag':tag,
        'grade':grade,
        'tests':tests,
        'students':students,
    }
    return render(request,'staff/grade-result.html',context)



@login_required(login_url='login')
def transfer(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    staff = Staff.objects.get(profile=pp)
    grades = Grade.objects.all()
    if request.method == 'POST':
        a = request.POST['grade']
        return redirect('st_transfering',id=a)
    context = {
        "web":web,
        'user':user,
        'staff':staff,'grades':grades,
    }
    return render(request,'staff/transfer/transfer.html',context)


@login_required(login_url='login')
def transfering(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    staff = Staff.objects.get(profile=pp)
    grades = Grade.objects.all().exclude(id=id)
    grade = Grade.objects.get(id=id)
    students = Student.objects.filter(grade=grade.name)
    if request.method == 'POST':
        if 'pass' in request.POST:
            items = request.POST.getlist('student')
            aa = request.POST['grade']
            to = Grade.objects.get(id=aa)
            for a in items:
                u = User.objects.get(id=a)
                p = Profile.objects.get(user=u)
                s = Student.objects.get(profile=p)
                save_student_history(s.id)
                p.grade = to
                p.save()
                s.grade = to.name
                s.save()
                messages.success(request,'students passed successfully!')
                return redirect('st_transfer')
        if 'fail' in request.POST:
            items = request.POST.getlist('student')
            for a in items:
                u = User.objects.get(id=a)
                p = Profile.objects.get(user=u)
                s = Student.objects.get(profile=p)
                save_student_history(s.id)
                messages.success(request,'students failed successfully!')
                return redirect('st_transfer')
    context = {
        "web":web,
        'user':user,
        'staff':staff,
        'grades':grades,
        'grade':grade,
        'students':students,
    }
    return render(request,'staff/transfer/transfering.html',context)



@login_required(login_url='login')
def edit(request,id):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    staff = Staff.objects.get(profile=pp)
    su = User.objects.get(id=id)
    pr = Profile.objects.get(user=su)
    st = Student.objects.get(profile=pr)
    grades = Grade.objects.all().exclude(id=pr.grade.id)
    if request.method == 'POST':
        if 'edit' in request.POST:
            if request.POST['first_name'] is not None:
                f = request.POST['first_name']
                su.first_name = f
                su.save()
                st.first_name = f
                st.save()
                messages.success(request,'you changed their first name successfully')
            if request.POST['last_name'] is not None:
                f = request.POST['last_name']
                su.last_name = f
                su.save()
                st.last_name = f
                st.save()
                messages.success(request,'you changed their last name successfully')
            if request.POST['email'] is not None:
                f = request.POST['email']
                su.email = f
                su.save()
                messages.success(request,'you changed their email successfully')
            if request.POST['grade'] is not None:
                f = request.POST['grade']
                gg = Grade.objects.get(id=f)
                pr.grade = gg
                pr.save()
                st.grade = gg.name
                st.save()
                messages.success(request,'you changed their grade successfully')
            return redirect('st_st_edit' , id=su.id)
        if 'verify' in request.POST:
            if st.is_verified == True:
                st.is_verified = False
                st.save()
                messages.success(request,'verification occured!')
            else:
                st.is_verified = True
                st.save()
                messages.success(request,'verification occured!')
            return redirect('st_st_edit' , id=su.id)
        if 'delete' in request.POST:
            su.delete()
            messages.success(request,'user deleted!')
            return redirect('r_index')
    context = {
        "web":web,
        'user':user,
        'staff':staff,
        'st':st,
        'grades':grades,
    }
    return render(request,'staff/edit.html',context)

@login_required(login_url='login')
def report_card_index(request):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    staff = Staff.objects.get(profile=pp)
    students = Student.objects.all()
    grades = Grade.objects.all()
    for a in students:
        a.full_name = a.first_name + a.last_name
        a.save()
    b=None
    if request.method == 'POST':
        b = request.POST['search']
        students = Student.objects.filter(full_name__icontains=b)
    context = {
        "web":web,
        'user':user,
        'staff':staff,
        'students':students,
        'a':b,
        'grades':grades,
    }
    if staff.report_card == True:
        return render(request,'staff/report card/index.html',context)
    else:
        messages.error(request,"Your not allowed to alter report card")
        return redirect('r_index')


@login_required(login_url='login')
def get_student_data(request,username):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    staff = Staff.objects.get(profile=pp)
    s_user = User.objects.get(username=username)
    s_profile = Profile.objects.get(user=s_user)
    student = Student.objects.get(profile=s_profile)
    his = History.objects.filter(user=s_user)
    counter = his.count() + 1
    cards = cardType.objects.all()
    if request.method == 'POST':
        a = request.POST['name']
        c = request.POST['id']
        st = Student.objects.get(pk=c)
        index1 = 1
        for c in range(0,StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-first_average').count()):
            a = StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-first_average')[c]
            a.first_rank = index1
            a.save() 
            if (c+1) < StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-first_average').count():
                next =  StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-first_average')[c+1]
                if next.first_average == a.first_average:
                    index1 = index1
                else:
                    index1=index1+1
        index2 = 1
        for c in range(0,StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-second_average').count()):
            a = StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-second_average')[c]
            a.second_rank = index2
            a.save() 
            if (c+1) < StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-second_average').count():
                next =  StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-second_average')[c+1]
                if next.second_average == a.second_average:
                    index2 = index2
                else:
                    index2=index2+1
        index3=1
        for c in range(0,StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-average').count()):
            a = StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-average')[c]
            a.rank = index3
            a.save() 
            if (c+1) < StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-average').count():
                next =  StudentStatus.objects.filter(time=st.year,grade=st.profile.grade).order_by('-average')[c+1]
                if next.average == a.average:
                    index3 = index3
                else:
                    index3=index3+1

        if cardType.objects.filter(name=a).exists():
            messages.error(request,"Name exists already")
        else:
            b = cardType.objects.create(name=a,user=user)
            messages.success(request,"created successfully")
            return redirect('t_add_card',st.id,b.id,AcademicYear.objects.last().id)
    context = {
        "web":web,
        'user':user,
        'staff':staff,
        'student':student,
        'his':his,
        'counter':counter,
        'cards':cards,
    }
    return render(request,'staff/report card/get-data.html',context)


@login_required(login_url='login')
def get_student_data_by_grade(request,grade):
    web = Webpack.objects.get(pk=1)
    user = request.user
    pp = Profile.objects.get(user=user)
    staff = Staff.objects.get(profile=pp)
    g = Grade.objects.get(id=grade)
    students = Student.objects.filter(grade=g)
    grades = Grade.objects.all()
    for a in students:
        a.full_name = a.first_name + a.last_name
        a.save()
    b=None
    if request.method == 'POST':
        b = request.POST['search']
        students = Student.objects.filter(full_name__icontains=b)
    context = {
        "web":web,
        'user':user,
        'staff':staff,
        'students':students,
        'a':b,
        'grades':grades,
    }
    if staff.report_card == True:
        return render(request,'staff/report card/grade-filter.html',context)
    else:
        messages.error(request,"Your not allowed to alter report card")
        return redirect('r_index')