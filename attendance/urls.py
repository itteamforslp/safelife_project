from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('<str:course_id>/<str:date>/', views.index, name='index'),
    path('<str:course_id>/<str:date>/updateStudent/', views.update_student, name='update_student'),
    path('<str:course_id>/<str:date>/updateStudentAbsent/', views.update_student_absent, name='update_student_absent'),
    #url(r'^(?P<course_id>\d+)/(?P<date>[\w|\W]+)/updateStudent/', views.update_student, name='updateStudent'),
    #url(r'^(?P<course_id>\d+)/(?P<date>[\w|\W]+)/updateStudentAbsent/', views.update_student_absent, name='update_student_absent'),
]
