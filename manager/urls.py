from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name="m_index"),
    path('rooms/',HomeRooms,name="m_room"),
    
    
    # Web Interface
    path('web/display/home/',displayweb,name="m_web_display"),#
    path('web/display/about/',displayabout,name="m_web_about"),#
    path('web/display/academic-info/',info,name="m_web_info"),#
    path('my-profile/',profile,name="m_profile"),#
    path('my-transfer/',laststudent,name="m_transfer"),#
    
    
    #data
    path('web/data/results/<str:year>/',resultdata,name="m_data_result"),
    path('web/data/results/by-test/get-<int:id>/',resultdatatest,name="m_data_result_test"),
    path('web/data/results/by-grade/get-<int:id>/',resultdatagrade,name="m_data_result_grade"),
    path('web/data/results/by-grade-student-of-year/student-id/student report card/student544527<int:id>7524233id/year4325684<year>6534422/',resultdatastudent,name="m_data_result_student"),
    path('web/data/results/by-term/get-<str:name>/',resultdataterm,name="m_data_result_term"),
    path('time/',time,name="m_time"),#
    path('events/',event,name="m_event"),#
    path('events/gallery-<int:id>',gallery,name="m_gallery"),#
    path('time/save/id-<int:id>/',savetime,name="m_time_save"),
    path('time/results/history/student/id-<int:id>/<str:year>/',resultdatahistory,name="m_history_student"),
    
    #blog
    path('web/blog/',blog,name="m_blog"),
    path('web/blog/add/',addblog,name="m_blog_add"),
    path('web/blog/add/to-<int:id>/',addsubblog,name="m_blog_add_sub"),
    path('web/blog/edit/blog-<int:id>/',editmainblog,name="m_blog_edit_main"),
    path('web/blog/edit/subblog-<int:id>/',editsubblog,name="m_blog_edit_sub"),
    path('web/blog/delete/blog-<int:id>/',deleteblog,name="m_blog_delete"),
    path('web/blog/delete/subblog-<int:id>/',deletesubblog,name="m_blog_delete_sub"),
    path('web/blog/delete/blog/category-<int:id>/',deletecategoryblog,name="m_blog_delete_category"),
    
    
    # User Interface
    path('data/user-data/',table,name="m_user_tabel"),#
    path('data/user-data/accept/users/',accepttable,name="m_user_accept_tabel"),#
    path('data/user-data/students/',studenttable,name="m_student_tabel"),#
    path('data/user-data/teachers/',teachertable,name="m_teacher_tabel"),#
    path('data/user-data/managers/',managertable,name="m_manager_tabel"),#
    path('data/user-data/students/<username>/edit/',studentedit,name="m_student_edit"),
    path('data/user-data/teachers/<username>/edit/',teacheredit,name="m_teacher_edit"),
    path('data/user-data/students/add/',studentadd,name="m_student_add"),#
    path('data/user-data/teachers/add/',teacheradd,name="m_teacher_add"),#
    path('data/user-data/managers/add/',manageradd,name="m_manager_add"),#
    path('data/user-data/user/delete/',deleteuser,name="m_user_delete"),
    path('data/user-data/user/accept/',acceptuser,name="m_user_accept"),
    
    
    # Staff Interface
    path('data/user-data/staff/edit/',staffedit,name="m_staff_edit"),
    path('data/user-data/staff/add/',staffadd,name="m_staff_add"),
]
