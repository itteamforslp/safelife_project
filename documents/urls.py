from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.default, name='default'),
    path('<int:doc_id>/', views.home, name='home'),
    url(r'^redirect/$', views.redirect, name='redirect'),
]