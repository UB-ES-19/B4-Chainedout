# Generated by Django 2.2.6 on 2019-12-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_chainedout', '0024_remove_profile_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='organizations',
            field=models.IntegerField(default=0),
        ),
    ]
