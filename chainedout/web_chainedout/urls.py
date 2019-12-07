from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
    path('profile/', views.save_profile, name='saveprofile'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_info, name="user_info"),
    path('profile/delete-education/<int:pk>', views.DeleteEducation.as_view(), name='delete_education'),
    path('profile/update-education/<int:pk>', views.UpdateEducation.as_view(), name='update_education'),
    path('profile/delete-experience//<int:pk>', views.DeleteExperience.as_view(), name='delete_experience'),
    path('profile/update-experience/<int:pk>', views.UpdateExperience.as_view(), name='update_experience'),
    path('profile/organization', views.request_organization, name='organization_info'),
    path('profile/update-profile/<int:pk>', views.UpdateProfile.as_view(), name='update_profile'),
    path('posts/', views.PostCreateView.as_view(), name='post_list'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/', views.post_info, name='post_info'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/like/', views.PostLike.as_view(), name='like_post'),
    path('posts/delete-post//<int:pk>', views.DeletePost.as_view(), name='delete_post'),
    path('posts/update-post/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/', views.UpdatePost.as_view(), name='update_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)