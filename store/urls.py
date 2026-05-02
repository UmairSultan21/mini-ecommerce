from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('products/', views.products, name='products'),

    path('orders/', views.orders, name='orders'),

    path('user/', views.user_home, name='user_home'),

    path('seller/', views.seller_home, name='seller_home'),

    path('dashboard/admin/', views.admin_home, name='admin_home'),  # FIXED

]