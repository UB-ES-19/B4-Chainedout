from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Follow(models.Model):
    user_following = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_followed = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = (['-date_created'])

    def __str__(self):
        return '{} follows {}'.format(self.user_following, self.user_followed)

User.add_to_class('following', models.ManyToManyField('self', through=Follow, related_name='followers', symmetrical=False))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.TextField(max_length=200, blank=True)
    #jobIds = models

"""
class Job(models.Model):

class Education(models.Model):
"""