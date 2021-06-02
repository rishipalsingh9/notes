from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_hello, name='get_hello'),
    path('contact/', views.get_contact, name='get_contact'),
    path('article/', views.get_article, name='get_article'),
    #path('your-name/', views.thanks, name='hello'),
    #path('thanks/', views.thanks, name='thanks'),
]
