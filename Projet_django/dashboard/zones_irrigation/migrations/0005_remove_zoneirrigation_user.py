# Generated by Django 4.2 on 2024-10-19 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zones_irrigation', '0004_zoneirrigation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zoneirrigation',
            name='user',
        ),
    ]
