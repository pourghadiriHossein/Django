from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list_view, name='posts_list'),
    path('<int:pk>/', views.post_detail_view, name='post_detail'),
    path('create/', views.post_create_view, name='create'),
    path('<int:pk>/update/', views.post_update_view, name='update'),
    path('<int:pk>/delete/', views.post_delete_view, name='delete'),
]