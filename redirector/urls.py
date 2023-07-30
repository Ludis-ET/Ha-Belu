from django.urls import path
from redirector.views import *


urlpatterns = [
    path('',index,name="r_index"),
    path('activate/<uidb64>/<token>',activate_user,name="activated"),
    path('resend-email/',resend,name="resend")
]
