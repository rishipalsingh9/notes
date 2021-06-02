from django.urls import path

from . import views

urlpatterns = [
    path('', views.authorform, name='addauthor'),
    path('addbook/', views.bookform, name='addbook'),
]
