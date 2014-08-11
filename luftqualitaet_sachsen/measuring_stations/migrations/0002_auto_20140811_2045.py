# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measuringpoint',
            options={'ordering': ['name'], 'verbose_name': 'Messstelle', 'verbose_name_plural': 'Messstellen'},
        ),
        migrations.AddField(
            model_name='measuringpoint',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
