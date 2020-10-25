from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('<int:course_id>/<str:date>/', views.index, name='index'),
    url(r'^(?P<course_id>\d+)/(?P<date>[\w|\W]+)/updateStudent/', views.update_student, name='update_student'),
    url(r'^(?P<course_id>\d+)/(?P<date>[\w|\W]+)/updateStudentAbsent/', views.update_student_absent, name='update_student_absent'),
]
