from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('user_profile/', views.Profile_view, name='user_profile'),
    path('user_profile_update/', views.Profile_view_update, name='user_profile_update'),
    path('view_orders/',views.view_orders,name='view_orders'),
]