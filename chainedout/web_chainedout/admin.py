from django.contrib import admin
# Register your models here.

from django.contrib import admin
from .models import Profile, Follow, Education, Experience, Post

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Post)