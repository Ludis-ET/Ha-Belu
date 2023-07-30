from django.contrib import admin
from .models import *

class BlogAdmin(admin.ModelAdmin):
    list_display = ('commenter','blog')
    search_fields = ('commenter','blog')


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('event','name')


class PasswordAdmin(admin.ModelAdmin):
    list_filter = ('sex','grade','level','type')
    list_display = ("first_name","last_name","password",'email','phone','sex','grade','level','type')
    search_fields  = ('first_name','last_name','email','sex','level','grade','phone','type')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',"phone",'sex',)
    search_fields = ('user','phone','sex',)
    list_filter = ('is_manager','is_teacher','is_student','sex',)


admin.site.register(Webpack)
admin.site.register(Event)
admin.site.register(Blog)
admin.site.register(Mainpage)
admin.site.register(About)
admin.site.register(Level)
admin.site.register(Grade)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Addblog)
admin.site.register(Password,PasswordAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Blog_comment,BlogAdmin)