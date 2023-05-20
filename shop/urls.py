from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('frequency-and-answer/', views.FAQView.as_view(), name='faq'),
    path('<int:pk>/product/', views.ProductView.as_view(), name='product'),
    path('<int:pk>/tag/', views.TagView.as_view(), name='tag'),
    path('<int:pk>/single-product/', views.SingleProductView.as_view(), name='singleProduct'),
    path('term-and-condition/', views.TACView.as_view(), name='tac'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/update-profile', views.UpdateProfileView.as_view(), name='update_profile'),
    path('dashboard/update-address/<int:pk>', views.UpdateAddressView.as_view(), name='update_address'),
    path('dashboard/delete-address/<int:pk>', views.DeleteAddressView.as_view(), name='delete_address'),
    path('dashboard/delete-comment/<int:pk>', views.DeleteCommentView.as_view(), name='delete_comment'),
]