# Generated by Django 4.2 on 2024-10-19 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zones_irrigation', '0006_zoneirrigation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='zoneirrigation',
            name='image_zone',
            field=models.ImageField(blank=True, null=True, upload_to='images_zones/'),
        ),
    ]
