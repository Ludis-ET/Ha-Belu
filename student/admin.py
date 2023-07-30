from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    search_fields = ('first_name','last_name','username','grade')
    list_display = ("id","profile",'first_name','last_name','username','grade','instagram','telegram')

class ChatAdmin(admin.ModelAdmin):
    search_fields = ('grade','sender')
    list_filter = ('grade','sender')
    list_display = ("message",'grade','sender','date')

class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ("course","message","sender")

class ResultHistoryAdmin(admin.ModelAdmin):
    list_display = ("status","student","name")

class ResultAdmin(admin.ModelAdmin):
    list_filter = ("subject","time")
    search_fields = ("student","name","status")
    list_display = ("student",'name','subject','status','time')

class SubjectResultAdmin(admin.ModelAdmin):
    list_filter = ("subject","time")
    search_fields = ("student","time","grade")
    list_display = ("student",'first','second','subject','grade')



admin.site.register(Student,StudentAdmin)
admin.site.register(Chat,ChatAdmin)
admin.site.register(Library)
admin.site.register(Course)
admin.site.register(Test)
admin.site.register(SubjectReslut,SubjectResultAdmin)
admin.site.register(StudentStatus)
admin.site.register(Result,ResultAdmin)
admin.site.register(ResultHistory,ResultHistoryAdmin)
admin.site.register(CourseComment,CourseCommentAdmin)