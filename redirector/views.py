from django.shortcuts import render,redirect
from home.models import *
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utils  import *
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from student.models import Student
from manager.models import Manager
from teacher.models import Teacher,Subject
from staff.models import Staff



def send_email(user,request):
    web = Webpack.objects.get(id=1)
    current_site = get_current_site(request)
    subject = "Activate your Account"
    body = render_to_string("redirect/authenticate.html",{
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



def index(request):
    web = Webpack.objects.get(id=1)
    user = request.user
    current_year = AcademicYear.objects.last()
    context = {
        'web':web,
    }
    if user.is_authenticated:
        if Profile.objects.filter(user=user):
            pp = Profile.objects.get(user=user)
            if pp.is_verified:
                if user.is_active:
                    if pp.is_student == True and pp.is_teacher == False and pp.is_manager == False and pp.is_staff == False:
                        student = Student.objects.get(profile=pp)
                        if student.year != current_year:
                            return redirect('s_year')
                        else:
                            if student.is_verified:
                                return redirect("s_index")
                            else:
                                return redirect("s_waiting")
                    elif pp.is_student == False and pp.is_teacher == True and pp.is_manager == False and pp.is_staff == False:
                        teacher = Teacher.objects.get(profile=pp)
                        if teacher.is_verified:
                            if teacher.subject is not None: 
                                return redirect("t_index")
                            else:
                                sss = Subject.objects.all()
                                ggg = Grade.objects.all()
                                if request.method == 'POST':
                                    a = request.POST['role']
                                    s = Subject.objects.get(id=a)
                                    teacher.subject = s
                                    teacher.save()
                                    select = request.POST.getlist('multiple')
                                    for aa in select:
                                        aaa = Grade.objects.get(id=aa) 
                                        teacher.my_room.add(aaa)
                                    teacher.save()
                                    return redirect('r_index')
                                return render(request,'redirect/subject.html',{'sss':sss,'ggg':ggg})
                        else:
                            return render(request,'student/waiting.html',{})
                    elif pp.is_student == False and pp.is_teacher == False and pp.is_manager == True and pp.is_staff == False:
                        teacher = Manager.objects.get(profile=pp)
                        if teacher.is_verified:
                            return redirect("m_index")
                        else:
                            return render(request,'student/waiting.html',{})
                    elif pp.is_student == False and pp.is_teacher == False and pp.is_manager == False and pp.is_staff == True:
                        staff = Staff.objects.get(profile=pp)
                        if staff.is_verified:
                            return redirect("st_index")
                        else:
                            return render(request,'student/waiting.html',{})
                    else:
                        return render(request,'redirect/invalid.html')
                else:
                    return render(request,'redirect/active.html')
            else:
                return render(request,'redirect/email.html',context)
        else:
            return render(request,'redirect/unknown.html',context)
    else:
        return redirect("a_index")


def activate_user(request,uidb64,token):
    uid=force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if account_activation_token.check_token(user,token):
        pp = Profile.objects.get(user=user)
        pp.is_verified = True
        pp.save()
        prof = Profile.objects.get(user=user)
        messages.success(request, "Email Activated Succesfully! we've sent you an email to confirm")
        subject = "Account Accepted"
        web = Webpack.objects.get(id=1)
        body = render_to_string("redirect/verified.html",{
            'user':user,
            'web':web,
        })
        main = strip_tags(body)
        email = EmailMultiAlternatives(subject=subject,body=main,from_email=settings.EMAIL_HOST_USER,to=[user.email],)
        email.attach_alternative(body,'text/html')
        email.send()
        return redirect('r_index')
    else:
        web = Webpack.objects.get(id=1)
        user = request.user
        context = {
            'web':web,
        }
        return render(request,'redirect/unverify.html',context)


@login_required(login_url='login')
def resend(request):
    user = request.user
    send_email(user,request)
    return redirect('r_index')