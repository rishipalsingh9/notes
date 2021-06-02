from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='packageregister'),
    path('createagent/', views.createagent, name='addagent')
]
