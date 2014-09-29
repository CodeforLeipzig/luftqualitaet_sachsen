# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0011_auto_20140929_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measuringpoint',
            name='form_id',
            field=models.IntegerField(unique=True, verbose_name='Formular ID'),
        ),
    ]
