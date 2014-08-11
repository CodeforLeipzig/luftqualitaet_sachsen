# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0003_auto_20140811_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measuringpoint',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
