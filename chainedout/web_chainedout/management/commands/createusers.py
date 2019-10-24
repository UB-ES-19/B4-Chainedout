from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of users to create')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            name = 'user' + str(i)
            user = User.objects.create_user(username=name, email='test@mail.com', password='password',
                                     first_name='First', last_name='Last')
        self.stdout.write("Created %s users" % total)