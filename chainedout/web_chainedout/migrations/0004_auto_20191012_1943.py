# Generated by Django 2.2.1 on 2019-10-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_chainedout', '0003_auto_20191012_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.AddField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]