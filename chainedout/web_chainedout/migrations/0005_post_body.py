# Generated by Django 2.2.5 on 2019-11-04 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_chainedout', '0004_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(default='Test'),
            preserve_default=False,
        ),
    ]
