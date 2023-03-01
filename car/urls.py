from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bmw/', views.bmw, name='bmw'),
    path('benz/', views.benz, name='benz'),
    path('dodge/', views.dodge, name='dodge'),
]
