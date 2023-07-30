from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name="t_index"),
    path('my/class/',all,name="t_all"),
    path('my/class/card/5464553442567347<id>5355344256734<id2>35534<id3>42567343/',addcard,name="t_add_card"),
    path('my/class/card/student-53553442567353<id>36655344256733-design-5355344256734<id2>3553442567<id3>343/',design,name="t_card"),
    path('my/class/card/student-53553442567353<id>36655344256733-design-5355344256734<id2>3553442567343<first>626525262<second>6/',dual,name="t_dual"),
    path('my/rooms/<teacher>2322424',room,name="t_room"),
    path('add/posts/',addpost,name="t_add_post"),
    path('add/course/',addcourse,name="t_add_course"),
    path('add/books/',addbook,name="t_add_book"),
    path('my/channel/',channel,name="t_channel"),
    path('my/profile/',TeacherProfile,name="t_profile"),
    path('my/channel/messages/',message,name="t_message"),
    path('my/channel/books/',books,name="t_books"),
    path('my/channel/edit/course/<int:id>/',editcourse,name="t_edit_course"),
    path('my/channel/edit/message/<int:id>/',editmessage,name="t_edit_message"),
    path('my/channel/edit/books/<int:id>/',editbook,name="t_edit_book"),
    path('my/channel/view/course/<int:id>/',myvideo,name="t_view_course"),
    path('my/channel/delete/course/',deletecourse,name="t_delete_course"),
    path('add/result/first/term/<int:id>/',oneresults,name="t_one_result"),
    path('add/result/second/term/<int:id>/',tworesults,name="t_two_result"),
    path('add/result/save/',saveresult,name="t_save_result")
]
