# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0012_auto_20140929_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='measuringpoint',
            name='ben',
            field=models.BooleanField(default=False, verbose_name='BEN'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='co',
            field=models.BooleanField(default=False, verbose_name='CO'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='ec',
            field=models.BooleanField(default=False, verbose_name='EC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='met',
            field=models.BooleanField(default=False, verbose_name='MET'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='no',
            field=models.BooleanField(default=False, verbose_name='NO'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='no2',
            field=models.BooleanField(default=False, verbose_name='NO2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='o3',
            field=models.BooleanField(default=False, verbose_name='O3'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='oc',
            field=models.BooleanField(default=False, verbose_name='OC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='pm10',
            field=models.BooleanField(default=False, verbose_name='PM10'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='pm10_pb',
            field=models.BooleanField(default=False, verbose_name='PM10 Pb'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='pm10_teom',
            field=models.BooleanField(default=False, verbose_name='PM10TEOM'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='pm25',
            field=models.BooleanField(default=False, verbose_name='PM2.5'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='so2',
            field=models.BooleanField(default=False, verbose_name='SO2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='sti',
            field=models.BooleanField(default=False, verbose_name='STI'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='stns',
            field=models.BooleanField(default=False, verbose_name='STNS'),
            preserve_default=True,
        ),
    ]
