from django.contrib import admin
# Register your models here.

from django.contrib import admin
from .models import Profile, Follow, Education, Experience, Post, Comment, Group, DeviceLog, PostImage, GroupPost, \
    GroupComment, GroupInvite, PrivateMessage

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(GroupPost)
admin.site.register(GroupComment)
admin.site.register(GroupInvite)
admin.site.register(PrivateMessage)
admin.site.register(DeviceLog)