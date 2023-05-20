from django.urls import path
from . import views

urlpatterns = [
    path('add-to-session/<int:pk>/', views.AddToSession.as_view(), name='add_to_session'),
    path('mines-from-session/<int:pk>/', views.MinesFromSession.as_view(), name='mines_from_session'),
    path('plus-from-session/<int:pk>/', views.PlusFromSession.as_view(), name='plus_from_session'),
    path('delete-item-from-session/<int:pk>/', views.DeleteItemFromSession.as_view(), name='delete_item_from_session'),
    path('add-discount/', views.AddToSession.as_view(), name='add_discount'),
]
