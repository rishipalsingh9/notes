from django.urls import path

from mdntuto import views

urlpatterns = [
    path('', views.index, name='index')
]
