from django.core.management.base import BaseCommand

from web_chainedout.models import Post


class Command(BaseCommand):
    help = 'Clear post database'

    def handle(self, *args, **options):
        Post.objects.all().delete()
        self.stdout.write("Deleted all posts from the database")
