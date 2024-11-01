# Generated by Django 4.2 on 2024-10-22 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommandation', '0002_alter_recommandation_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommandation',
            name='cout_estime',
        ),
        migrations.RemoveField(
            model_name='recommandation',
            name='frequence_repetition',
        ),
        migrations.AddField(
            model_name='recommandation',
            name='average_temperature',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='recommandation',
            name='crop_type',
            field=models.CharField(default='Inconnu', max_length=100),
        ),
        migrations.AddField(
            model_name='recommandation',
            name='region',
            field=models.CharField(default='Sousse', max_length=100),
        ),
        migrations.AddField(
            model_name='recommandation',
            name='total_precipitation',
            field=models.FloatField(default=20),
        ),
    ]
