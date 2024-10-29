# Generated by Django 4.2.6 on 2024-10-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capteurs', '0004_mesure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mesure',
            old_name='humidity',
            new_name='moisture',
        ),
        migrations.AddField(
            model_name='mesure',
            name='should_irrigate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='capteur',
            name='date_installation',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='capteur',
            name='localisation',
            field=models.CharField(default='Tunisie', max_length=100),
        ),
    ]
