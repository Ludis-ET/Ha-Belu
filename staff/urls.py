from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="st_index"),
    path("students-result/alter/", result, name="st_result"),
    path("students-result/alter-grade-id-726626262<id>7162626/", grade_result, name="st_grade_result"),
    path("transfer-students/", transfer, name="st_transfer"),
    path("transfer-students/from-grade-6355252<id>7736", transfering, name="st_transfering"),
    path("student/report-card/", report_card_index, name="st_report_card_index"),
    path("student/report-card/get-data/username-@<username>", get_student_data, name="st_get_studet_data"),
    path("student/report-card/edit/id-867764<id>584884", edit, name="st_st_edit"),
    path("student/report-card/get-data/grade-<grade>", get_student_data_by_grade, name="st_get_studet_data_by_grade"),
]
