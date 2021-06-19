from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('supplier/', views.supplier, name='supplier'),
    path('agent/', views.agent, name='agent'),
    path('hotel/', views.hotel, name='hotel'),
]