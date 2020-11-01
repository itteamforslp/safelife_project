from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='administrator-home'),
    url(r'^updateCourseNotes', views.update_course_notes, name='update_course_notes'),
]