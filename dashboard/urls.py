from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('dashboard-2/',views.dashboard2,name='dashboard2'),
    path('products/product_list/',views.product_list,name='product_list'),
    path('products/product_create/',views.product_create,name='product_create'),
    path('products/product_update/<int:pk>/',views.product_update,name='product_update'),
    path('product_delete/<int:pk>/',views.product_delete,name='product_delete'),

    # product Variant
    path('variants/variant_list/',views.variant_list,name='variant_list'),
    path('variants/add_variant',views.add_variant,name='add_variant'),
    path('variants/variant_update/<int:pk>/',views.variant_update,name='variant_update'),
    path('variant_delete/<int:pk>/',views.variant_delete,name='variant_delete'),

    # Category
    path('categories/category_list/',views.category_list,name='category_list'),
    path('categories/add_category/',views.add_category,name='add_category'),
    path('categories/category_update/<int:pk>/',views.category_update,name='category_update'),
    path('category_delete/<int:pk>/',views.category_delete,name='category_delete'),

    #User
    path('users/user_list/',views.user_list,name='user_list'),
    # path('add_user/',views.add_user,name='add_user'),
    path('users/user_update/<int:pk>/',views.user_update,name='user_update'),
    path('user_deactivate/<int:pk>/',views.user_deactivate,name='user_deactivate'),

    # Order
    path('orders/order_list',views.order_list,name='order_list'),
    path('orders/order_detail/<int:order_id>/',views.order_detail,name='order_detail'),

]
