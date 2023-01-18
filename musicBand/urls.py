from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('BTS/', views.BTS, name='BTS'),
    path('Queen/', views.Queen, name='Queen'),
    path('Pink-Floyd/', views.Pink_Floyd, name='Pink_Floyd'),
]