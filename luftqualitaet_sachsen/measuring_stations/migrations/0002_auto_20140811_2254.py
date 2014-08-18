# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicatedvalue',
            name='unit',
            field=models.CharField(default='SO2', max_length=10, verbose_name='Einheit', choices=[('SO2', 'SO2'), ('NO', 'NO'), ('NO2', 'NO2'), ('O3', 'O3'), ('BEN', 'BEN'), ('PM10TEOM', 'PM10 TEOM'), ('PM10', 'PM10'), ('PM2.5', 'PM2.5'), ('EC', 'EC'), ('OC', 'OC'), ('STI', 'ST-I'), ('STNS', 'ST-NS'), ('MET', 'Met.')]),
        ),
    ]
