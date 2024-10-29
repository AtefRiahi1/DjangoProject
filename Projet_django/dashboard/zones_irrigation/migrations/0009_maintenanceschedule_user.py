# Generated by Django 4.2 on 2024-10-28 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zones_irrigation', '0008_alter_zoneirrigation_besoin_eau_maintenanceschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenanceschedule',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
