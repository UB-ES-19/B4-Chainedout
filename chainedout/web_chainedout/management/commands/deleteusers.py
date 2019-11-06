from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Clear user database'

    def handle(self, *args, **options):
        User.objects.all().delete()
        self.stdout.write("Deleted all users from the database")
