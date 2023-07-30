from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
import debug_toolbar
from django.conf.urls import handler400, handler403, handler404, handler500




urlpatterns = [
    
    path('admin-ludis/', admin.site.urls),
    path('',include('redirector.urls'),name="redirect"),
    path('home/',include('home.urls'),name="home"),
    path('student/',include('student.urls'),name="student"),
    path('teacher/',include('teacher.urls'),name="teacher"),
    path('manager/',include('manager.urls'),name="manager"),
    path('staff/',include('staff.urls'),name="staff"),


    re_path(r'^__debug__/', include(debug_toolbar.urls)),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'
handler400 = 'home.views.handler400'
handler403 = 'home.views.handler403'