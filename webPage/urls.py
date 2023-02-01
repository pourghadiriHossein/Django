from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('hcj/', views.show_hcj_page, name='hcj'),
    path('django/', views.show_django_page, name='django'),
    path('laravel/', views.show_laravel_page, name='laravel'),
]