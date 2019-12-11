from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


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


class Education(models.Model):
    entity = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    edu_started = models.IntegerField(default=2019)
    edu_finished = models.IntegerField(default=2020)


class Experience(models.Model):
    work_experience = models.TextField(max_length=50)
    company = models.CharField(max_length=50)
    exp_started = models.IntegerField(default=2019)
    exp_finished = models.IntegerField(default=2020)
    job = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.TextField(max_length=500)
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=200)
    skills = models.TextField(max_length=500)
    birth_date = models.DateField(null=True)
    jobIds = models.IntegerField(default=0)
    achievements = models.TextField(max_length=500)
    phone = models.IntegerField(default=0)
    website = models.CharField(max_length=50, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    educations = models.ManyToManyField(Education)
    experiences = models.ManyToManyField(Experience)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Post(models.Model):
    STATUS = (('draft', 'Draft'), ('posted', 'Posted'))
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='posts/images')
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_info',
                       args=[self.published.year, self.published.month, self.published.day, self.slug, self.pk])


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/images', verbose_name="Image")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default="", related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)


class Group(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='groups/images')
    members = models.ManyToManyField(User, blank=True, related_name='user_groups')

    def get_absolute_url(self):
        return reverse('group-profile',
                       args=[self.pk])

    def __str__(self):
        return self.name


class GroupPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='group_posts/images')
    published = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='group_post_likes')

    class Meta:
        ordering = ('-published',)

    def get_absolute_url(self):
        return reverse('group_post_info', args=[self.group.pk, self.pk])


class GroupComment(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_comments')
    body = models.CharField(max_length=250)
    published = models.DateTimeField(default=timezone.now)


class GroupInvite(models.Model):
    text = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invites')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites_received')
    created = models.DateTimeField(default=timezone.now)
