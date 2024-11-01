# Generated by Django 4.2 on 2024-10-13 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_passwordresettoken_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Editor', 'Editor'), ('Client', 'Client')], max_length=255, null=True, verbose_name='Role'),
        ),
    ]
