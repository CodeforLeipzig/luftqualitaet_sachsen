# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeasuringPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('location', models.CharField(max_length=100, verbose_name='Standort')),
                ('amsl', models.IntegerField(null=True, verbose_name='H\xf6he \xfcber NN [m]', blank=True)),
                ('eu_typing', models.IntegerField(default=1, verbose_name='Typisierung nach EU- Richtlinie', choices=[(1, 'st\xe4dtischer Hintergrund'), (2, 'st\xe4dtisch/Verkehr'), (3, 'vorst\xe4dtisches Gebiet'), (4, 'l\xe4ndlich, stadtnah'), (5, 'l\xe4ndlich'), (6, 'l\xe4ndlicher Hintergrund'), (7, 'H\xf6henstation')])),
                ('category', models.IntegerField(default=2, verbose_name='Kategorie', choices=[(1, 'Stationen zur Beurteilung der regionalen Vorbelastung'), (2, 'Stationen zur Beurteilung der allgemeinen st\xe4dtischen Belastung'), (3, 'Stationen zur Beurteilung verkehrsnaher Belastungen')])),
                ('image', models.ImageField(upload_to='measuring_stations', verbose_name='Bild', blank=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
            ],
            options={
                'verbose_name': 'Messstelle',
                'verbose_name_plural': 'Messstellen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndicatedValue',
            fields=[
                ('uuid', uuidfield.fields.UUIDField(primary_key=True, serialize=False, editable=False, max_length=32, blank=True, unique=True)),
                ('value', models.FloatField(verbose_name='Wert')),
                ('unit', models.IntegerField(default=1, verbose_name='Einheit', choices=[(1, 'SO2'), (2, 'NOX'), (3, 'O3'), (4, 'BTX'), (5, 'PM10 TEOM'), (6, 'PM10'), (7, 'PM2,5'), (8, 'EC'), (9, 'OC'), (10, 'ST-I'), (11, 'ST-NS'), (12, 'Met.')])),
                ('date_created', models.DateTimeField(verbose_name='Erstellt am')),
                ('measuring_point', models.ForeignKey(to='measuring_stations.MeasuringPoint', to_field='id', verbose_name='Messstelle')),
            ],
            options={
                'ordering': ['-date_created'],
                'verbose_name': 'Messwert',
                'verbose_name_plural': 'Messwerte',
            },
            bases=(models.Model,),
        ),
    ]
