from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_info, name="user_info"),
]