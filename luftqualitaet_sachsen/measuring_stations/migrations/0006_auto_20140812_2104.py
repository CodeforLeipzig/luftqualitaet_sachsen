# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='measuringpoint',
            name='city',
            field=models.CharField(default='', help_text='Stadt oder Ortschaft angeben', max_length=100, verbose_name='Stadt'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='measuringpoint',
            name='eu_typing',
            field=models.IntegerField(default=1, verbose_name='Typisierung nach EU-Richtlinie', choices=[(1, 'st\xe4dtischer Hintergrund'), (2, 'st\xe4dtisch/Verkehr'), (3, 'vorst\xe4dtisches Gebiet'), (4, 'l\xe4ndlich, stadtnah'), (5, 'l\xe4ndlich'), (6, 'l\xe4ndlicher Hintergrund'), (7, 'H\xf6henstation')]),
        ),
        migrations.AlterField(
            model_name='measuringpoint',
            name='location',
            field=models.CharField(help_text='Sta\xdfe bzw. ungef\xe4hren Standort angeben', max_length=100, verbose_name='Standort'),
        ),
    ]
