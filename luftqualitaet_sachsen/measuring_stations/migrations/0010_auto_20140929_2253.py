# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0009_auto_20140922_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='measuringpoint',
            name='form_id',
            field=models.IntegerField(default=0, verbose_name='Formular ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='indicatedvalue',
            name='date_created',
            field=models.DateTimeField(verbose_name='Datum'),
        ),
        migrations.AlterField(
            model_name='indicatedvalue',
            name='measuring_point',
            field=models.ForeignKey(related_name='indicated_values', verbose_name='Messstelle', to='measuring_stations.MeasuringPoint'),
        ),
    ]
