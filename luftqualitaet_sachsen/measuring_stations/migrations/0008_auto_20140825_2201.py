# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicatedvalue',
            name='ben',
            field=models.FloatField(default=0, verbose_name='BEN'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='co',
            field=models.FloatField(default=0, verbose_name='CO'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='ec',
            field=models.FloatField(default=0, verbose_name='EC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='met',
            field=models.FloatField(default=0, verbose_name='MET'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='no',
            field=models.FloatField(default=0, verbose_name='NO'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='no2',
            field=models.FloatField(default=0, verbose_name='NO2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='o3',
            field=models.FloatField(default=0, verbose_name='O3'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='oc',
            field=models.FloatField(default=0, verbose_name='OC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='pm10',
            field=models.FloatField(default=0, verbose_name='PM10'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='pm10_pb',
            field=models.FloatField(default=0, verbose_name='PM10 Pb'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='pm10_teom',
            field=models.FloatField(default=0, verbose_name='PM10TEOM'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='pm25',
            field=models.FloatField(default=0, verbose_name='PM2.5'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='so2',
            field=models.FloatField(default=0, verbose_name='SO2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='sti',
            field=models.FloatField(default=0, verbose_name='STI'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicatedvalue',
            name='stns',
            field=models.FloatField(default=0, verbose_name='STNS'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='indicatedvalue',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='indicatedvalue',
            name='value',
        ),
    ]
