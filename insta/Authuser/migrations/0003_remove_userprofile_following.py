# Generated by Django 5.0.1 on 2024-03-24 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authuser', '0002_userprofile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='following',
        ),
    ]