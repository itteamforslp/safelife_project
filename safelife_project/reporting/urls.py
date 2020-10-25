from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('<int:course_id>/', views.report, name ='reports'),
    path('<int:course_id>/<int:month>/', views.report, name='reports'),
    path('', views.index, name='index'),
    path('', views.report, name='teacher-reporting'),
    #path('<int:course_id>/', views.index, name='reports'),
    #path('success/', views.success, name = 'success'),   
]
