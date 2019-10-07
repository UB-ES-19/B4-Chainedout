from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
    path('profile/', views.testprofile, name='testprofile'),
]
