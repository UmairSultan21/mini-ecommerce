from django.urls import path
from . import views

urlpatterns = [

    # ================= BASIC =================
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('orders/', views.orders, name='orders'),

    # ================= USER =================
    path('user/', views.user_home, name='user_home'),

    # ================= ROLE DASHBOARDS =================
    path('seller/', views.seller_home, name='seller_home'),
    path('admin/dashboard/', views.admin_home, name='admin_home'),

    # ================= PRODUCT =================
    path('add_product/', views.add_product, name='add_product'),

    # ================= CART =================
    path('cart/', views.cart_page, name='user_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # ================= WISHLIST =================
    path('wishlist/', views.wishlist_page, name='user_wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]