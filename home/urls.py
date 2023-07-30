from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="a_index"),
    path("about/", about, name="a_about"),
    path("teachers/", teacher, name="a_teacher"),
    path("contacts/", contact, name="a_contact"),
    path("blog/", blog, name="a_blog"),
    path("login/", login_page, name="login"),
    path("password-reset/", passReset, name="reset"),
    path("logout/", custom_logout, name="logout"),
    path("register/", register_user, name="register"),
    path("blog-search/", blog_search, name="blog_search"),
    path("blog-post/<int:id>/", blog_post, name="blog_post"),
    path("blog-post/category/<int:id>/", category, name="category"),
    path("events/<int:id>/", event, name="event"),
    path('forget/<uidb64>/<token>',forget_password,name="forgeted"),
]
