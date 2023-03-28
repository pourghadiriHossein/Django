from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_view, name="book_list"),
    path('<int:pk>/', views.book_detail_view, name="book_detail"),
    path('create/', views.book_create_view, name="book_create"),
    path('<int:pk>/update/', views.book_update_view, name="book_update"),
    path('<int:pk>/delete/', views.book_delete_view, name="book_delete"),
]
