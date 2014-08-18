# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.template.defaultfilters import slugify


def add_slug(apps, schema_editor):
    MeasuringPoint = apps.get_model('measuring_stations', 'MeasuringPoint')
    for measuring_point in MeasuringPoint.objects.all():
        measuring_point.slug = slugify(measuring_point.name)
        measuring_point.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('measuring_stations', '0002_auto_20140811_2045'),
    ]
    operations = [
        migrations.RunPython(add_slug, backwards)
    ]
