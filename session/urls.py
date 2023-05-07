from django.urls import path
from . import views

urlpatterns = [
    path('add-to-session/<int:pk>/', views.add_to_session, name='add_to_session'),
    path('mines-from-session/<int:pk>/', views.mines_from_session, name='mines_from_session'),
    path('plus-from-session/<int:pk>/', views.plus_from_session, name='plus_from_session'),
    path('delete-item-from-session/<int:pk>/', views.delete_item_from_session, name='delete_item_from_session'),
    path('add-discount/', views.add_discount, name='add_discount'),
]
