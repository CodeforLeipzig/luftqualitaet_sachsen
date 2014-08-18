# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('measuring_stations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measuringpoint',
            options={'ordering': ['name'], 'verbose_name': 'Messstelle', 'verbose_name_plural': 'Messstellen'},
        ),
        migrations.AlterField(
            model_name='measuringpoint',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='measuring_stations', verbose_name='Bild', blank=True),
        ),
    ]
