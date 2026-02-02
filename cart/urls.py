from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    # Note: product_id hata diya gaya hai
    path('increase/<int:variant_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:variant_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:variant_id>/', views.remove_from_cart, name='remove_from_cart'),
]