from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('register-group/', views.register_group, name='register-group'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
    path('profile/', views.save_profile, name='saveprofile'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/', views.user_list, name='user_list'),
    path('users/<group>', views.group_user_list, name='group_user_list'),
    path('users/<username>/', views.user_info, name="user_info"),
    path('profile/delete-education/<int:pk>', views.DeleteEducation.as_view(), name='delete_education'),
    path('profile/update-education/<int:pk>', views.UpdateEducation.as_view(), name='update_education'),
    path('profile/delete-experience//<int:pk>', views.DeleteExperience.as_view(), name='delete_experience'),
    path('profile/update-experience/<int:pk>', views.UpdateExperience.as_view(), name='update_experience'),
    path('profile/update-profile/<int:pk>', views.UpdateProfile.as_view(), name='update_profile'),
    path('posts/', views.PostCreateView.as_view(), name='post_list'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/', views.post_info, name='post_info'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/like/', views.PostLike.as_view(), name='like_post'),
    path('posts/delete-post/<int:pk>', views.DeletePost.as_view(), name='delete_post'),
    path('posts/update-post/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/', views.UpdatePost.as_view(), name='update_post'),
    path('summernote/', include('django_summernote.urls')),
    path('group-profile/<int:pk>', views.group_profile, name='group-profile'),
    path('group-profile/<int:group_pk>/<int:post_pk>/', views.group_post_info, name='group_post_info'),
    path('group-profile/<int:group_pk>/<int:post_pk>/like/', views.GroupPostLike.as_view(), name='group_post_like'),
    path('group-profile/<int:group_pk>/update-post/<int:post_pk>', views.UpdateGroupPost.as_view(), name='update_group_post'),
    path('group-profile/<int:group_pk>/delete-post/<int:pk>', views.DeleteGroupPost.as_view(), name='delete_group_post'),
    path('groups/', views.groups, name='groups'),
    path('groups/update-group/<int:pk>', views.UpdateGroup.as_view(), name='update_group'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)