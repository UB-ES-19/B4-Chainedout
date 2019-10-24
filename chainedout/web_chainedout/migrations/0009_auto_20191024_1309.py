# Generated by Django 2.2.5 on 2019-10-24 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_chainedout', '0008_auto_20191024_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='user',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='educations',
            field=models.ManyToManyField(to='web_chainedout.Education'),
        ),
        migrations.AddField(
            model_name='profile',
            name='experiences',
            field=models.ManyToManyField(to='web_chainedout.Experience'),
        ),
    ]
