# Generated by Django 2.2.5 on 2019-11-04 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_chainedout', '0003_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=12231231, max_length=500, unique_for_date='published'),
            preserve_default=False,
        ),
    ]
