# Generated by Django 4.0.2 on 2022-03-13 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_user_is_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_online',
        ),
    ]