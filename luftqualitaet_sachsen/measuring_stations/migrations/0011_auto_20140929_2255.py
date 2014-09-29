# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_form_id(apps, schema_editor):
    MeasuringPoint = apps.get_model('measuring_stations', 'MeasuringPoint')
    for measuring_point in MeasuringPoint.objects.all():
        measuring_point.form_id = measuring_point.id
        measuring_point.save()


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0010_auto_20140929_2253'),
    ]

    operations = [
        migrations.RunPython(add_form_id),
    ]
