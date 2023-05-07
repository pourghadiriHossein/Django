from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),
]