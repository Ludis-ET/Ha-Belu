from django.contrib import admin
from .models import *


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("profile",'instagram','telegram')


admin.site.register(Teacher,TeacherAdmin)
admin.site.register(GradePost)
admin.site.register(Subject)
admin.site.register(HomeRoom)
admin.site.register(cardType)
admin.site.register(CTable)
admin.site.register(StudentGrade)
admin.site.register(StudentName)
admin.site.register(icon)
admin.site.register(Text)
admin.site.register(Line)