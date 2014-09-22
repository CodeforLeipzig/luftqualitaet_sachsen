# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0008_auto_20140825_2201'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='indicatedvalue',
            unique_together=set([('date_created', 'measuring_point')]),
        ),
    ]
