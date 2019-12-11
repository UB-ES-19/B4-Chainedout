# Generated by Django 2.2.5 on 2019-12-11 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_chainedout', '0028_profile_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(max_length=50)),
                ('compan', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=200)),
                ('until', models.IntegerField(default=2021)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='name_organization',
            field=models.CharField(default='Name Organization', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='job',
            field=models.ManyToManyField(to='web_chainedout.Job'),
        ),
    ]
