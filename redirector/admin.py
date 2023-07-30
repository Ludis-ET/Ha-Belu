from django.contrib import admin
from .models import *


class HistoryAdmin(admin.ModelAdmin):
    list_display = ("user","academicYear","first_name","last_name","phone","instagram","telegram")
    list_filter = ("is_student","sex","grade","academicYear")
    search_fields = ("first_name","last_name","academicYear","user","phone")

class yearAdmin(admin.ModelAdmin):
    list_display = ("year","id")


admin.site.register(AcademicYear,yearAdmin)
admin.site.register(History,HistoryAdmin)
admin.site.register(TestHistory)
admin.site.register(SubjectReslutHistory)
admin.site.register(StudentStatusHistory)