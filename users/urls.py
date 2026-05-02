from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_view, name='login'),

    path('register/', views.register, name='register'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),

    path('profile/', views.profile, name='profile'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
]