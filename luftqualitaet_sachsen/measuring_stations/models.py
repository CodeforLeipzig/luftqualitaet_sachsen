# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from geoposition.fields import GeopositionField
from uuidfield import UUIDField


@python_2_unicode_compatible
class MeasuringPoint(models.Model):
    EU_TYPING_CITY_BACKGROUND = 1
    EU_TYPING_CITY_TRAFFIC = 2
    EU_TYPING_SUBURBAN = 3
    EU_TYPING_RURAL_CLOSE_TO_CITY = 4
    EU_TYPING_RURAL = 5
    EU_TYPING_RURAL_BACKGROUND = 6
    EU_TYPING_HEIGHT_STATION = 7
    EU_TYPING_CHOICES = (
        (EU_TYPING_CITY_BACKGROUND, 'städtischer Hintergrund'),
        (EU_TYPING_CITY_TRAFFIC, 'städtisch/Verkehr'),
        (EU_TYPING_SUBURBAN, 'vorstädtisches Gebiet'),
        (EU_TYPING_RURAL_CLOSE_TO_CITY, 'ländlich, stadtnah'),
        (EU_TYPING_RURAL, 'ländlich'),
        (EU_TYPING_RURAL_BACKGROUND, 'ländlicher Hintergrund'),
        (EU_TYPING_HEIGHT_STATION, 'Höhenstation'),
    )
    CATEGORY_LOCAL = 1
    CATEGORY_CITY = 2
    CATEGORY_TRAFFIC = 3
    CATEGORIES = (
        (CATEGORY_LOCAL, 'Stationen zur Beurteilung der regionalen Vorbelastung'),
        (CATEGORY_CITY, 'Stationen zur Beurteilung der allgemeinen städtischen Belastung'),
        (CATEGORY_TRAFFIC, 'Stationen zur Beurteilung verkehrsnaher Belastungen'),
    )
    name = models.CharField('Name', max_length=100, unique=True)
    location = models.CharField('Standort', max_length=100)
    amsl = models.IntegerField('Höhe über NN [m]', blank=True, null=True)
    eu_typing = models.IntegerField('Typisierung nach EU- Richtlinie', choices=EU_TYPING_CHOICES,
        default=EU_TYPING_CITY_BACKGROUND)
    category = models.IntegerField('Kategorie', choices=CATEGORIES, default=CATEGORY_CITY)
    image = models.ImageField('Bild', upload_to='measuring_stations', blank=True)
    position = GeopositionField()

    class Meta:
        verbose_name = 'Messstelle'
        verbose_name_plural = 'Messstellen'
        ordering = ['name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class IndicatedValue(models.Model):
    SO2 = 'SO2'
    NO = 'NO'
    NO2 = 'NO2'
    O3 = 'O3'
    BEN = 'BEN'
    PM10_TEOM = 'PM10TEOM'
    PM10 = 'PM10'
    PM25 = 'PM2.5'
    EC = 'EC'
    OC = 'OC'
    STI = 'STI'
    STNS = 'STNS'
    MET = 'MET'
    UNITS = (
        (SO2, 'SO2'),
        (NO, 'NO'),
        (NO2, 'NO2'),
        (O3, 'O3'),
        (BEN, 'BEN'),
        (PM10_TEOM, 'PM10 TEOM'),
        (PM10, 'PM10'),
        (PM25, 'PM2.5'),
        (EC, 'EC'),
        (OC, 'OC'),
        (STI, 'ST-I'),
        (STNS, 'ST-NS'),
        (MET, 'Met.'),
    )
    uuid = UUIDField(auto=True, primary_key=True)
    value = models.FloatField('Wert')
    unit = models.CharField('Einheit', choices=UNITS, default=SO2, max_length=10)
    date_created = models.DateTimeField('Erstellt am')
    measuring_point = models.ForeignKey(MeasuringPoint, related_name='indicated_values',
        verbose_name='Messstelle')

    class Meta:
        verbose_name = 'Messwert'
        verbose_name_plural = 'Messwerte'
        ordering = ['-date_created']

    def __str__(self):
        return '%s %s' % (self.value, self.unit)

    def save(self, *args, **kwargs):
        #if not self.uuid:
            #self.date_created = now()
        super(IndicatedValue, self).save(*args, **kwargs)
