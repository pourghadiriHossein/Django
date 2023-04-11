from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('frequency-and-answer/', views.frequency_and_answer, name='faq'),
    path('<int:pk>/product/', views.product, name='product'),
    path('<int:pk>/tag/', views.tag, name='tag'),
    path('<int:pk>/single-product/', views.single_product, name='singleProduct'),
    path('term-and-condition/', views.term_and_condition, name='tac'),
    path('dashboard/', views.dashboard, name='dashboard'),
]