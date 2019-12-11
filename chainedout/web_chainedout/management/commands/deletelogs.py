from django.core.management.base import BaseCommand

from web_chainedout.models import DeviceLog


class Command(BaseCommand):
    help = 'Clear log database'

    def handle(self, *args, **options):
        DeviceLog.objects.all().delete()
        self.stdout.write("Deleted all logs from the database")
