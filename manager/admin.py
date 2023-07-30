from django.contrib import admin
from .models import *


class ManagerAdmin(admin.ModelAdmin):
    list_display = ("profile",'instagram','telegram')


admin.site.register(Manager,ManagerAdmin)
admin.site.register(StudentMessage)