from django.urls import path
from . import views


urlpatterns = [
   
    path('category_page/<int:cat_id>/',views.category_page,name='category_page'),
    path('product/',views.product_list,name='product'),
    path('product_details_page/<slug:slug>/',views.product_details_page,name='product_details_page'),
    path('wishlist_page/', views.wishlist_page, name='wishlist_page'),
    path('wishlist_view/', views.wishlist_view, name='wishlist_view'),
    # path('filter/',views.filter_price,name='filter_price'),
]