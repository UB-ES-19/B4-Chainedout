from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from random import randint
from django.db.models.aggregates import Count
from django.template.defaultfilters import slugify

from web_chainedout.models import Post


class Command(BaseCommand):
    help = 'Create random posts'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of users to create')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            title = get_random_string(length=10)
            post = Post.objects.create(title=title, author=self.random(), slug=slugify(title),
                                       body=get_random_string(length=200), status='posted')
        self.stdout.write("Created %s posts" % total)

    def random(self):
        count = User.objects.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return User.objects.all()[random_index]