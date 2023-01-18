from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ronaldo/', views.ronaldo, name='ronaldo'),
    path('messi/', views.messi, name='messi'),
    path('karim/', views.karim, name='karim'),
]