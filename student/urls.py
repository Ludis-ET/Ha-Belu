from django.urls import path,re_path
from .views import *


urlpatterns = [
    path('',index,name="s_index"),
    path('chatting/',chatting,name="s_chat"),
    path('chatting/search/',searchStudent,name="s_search"),
    path('library/',Books,name="library"),
    path('waiting/',waiting,name="s_waiting"),
    path('invalid-year-address/',year,name="s_year"),
    path('get-data-of/<str:year>/history/<str:username>/',year_history,name="s_year_history"),
    path('my-profile/',StudentProfile,name="s_profile"),
    path('courses/',Courses,name="course"),
    path('delete-account/<int:id>/',deleteaccount,name="delete_account"),
    path('courses/<int:id>/video-stream/',page,name="page"),
    path('courses/<int:id>/subject/',subject,name="c_subject"),
    path('academic/status/',result,name="s_result"),
    path('academic/status/history/',his,name="s_history"),
    path('academic/status/history/<year>',Historyresult,name="s_result_history"),
    path('courses/search',Coursesearch,name="course_search"),
    path('courses/teacher/<int:id>/',teacher,name="s_teacher"),
    path('courses/teacher/<int:id>/messages',teachermessage,name="s_teacher_message"),
    path('courses/teacher/<int:id>/books',teacherbook,name="s_teacher_books"),
    re_path(r'^view-profile-of/(?P<username>\w+)/$',users,name='s_users'),
    re_path(r'^get-chat-with/(?P<username>\w+)/$',getChat,name='get_chat'),
]
