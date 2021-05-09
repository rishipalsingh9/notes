from django.urls import path

from catalog import views


urlpatterns = [
    path('catalog/', views.index, name='index')
]
