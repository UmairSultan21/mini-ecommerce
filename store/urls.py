from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('products/', views.products, name='products'),

    path('orders/', views.orders, name='orders'),

    path('user/', views.user_home, name='user_home'),

    path('seller/', views.seller_home, name='seller_home'),

    path('dashboard/admin/', views.admin_home, name='admin_home'),  # FIXED

    path('add_product/', views.add_product, name='add_product'),

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('wishlist/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]