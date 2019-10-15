from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Follow(models.Model):
    user_following = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_followed = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = (['-date_created'])

    def __str__(self):
        return '{} follows {}'.format(self.user_following, self.user_followed)


User.add_to_class('following',
                  models.ManyToManyField('self', through=Follow, related_name='followers', symmetrical=False))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.TextField(max_length=50)
    bio = models.TextField(max_length=500)
    location = models.TextField(max_length=200)
    education = models.TextField(max_length=300)
    skills = models.TextField(max_length=400)
    jobIds = models.IntegerField(default=0)
    achievements = models.TextField(max_length=500)
    experience = models.TextField(max_length=500)
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

"""
    class Job(models.Model):

    class Education(models.Model):

    class Skills(models.Model):

    class Achievements(models.Model):

"""
