# Generated by Django 2.2.1 on 2019-10-12 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_chainedout', '0002_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='birthdate',
            new_name='birth_date',
        ),
    ]
