#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

import gevent.monkey
import requests
from django.core.management.base import BaseCommand
from optparse import make_option
from HTMLParser import HTMLParser

from srtm import get_data
from geoposition.fields import Geoposition
from geopy.geocoders import Nominatim
from decimal import Decimal

from ...models import MeasuringPoint


class Command(BaseCommand):
    args = ''
    help = 'Fetches a list of stations from www.umweltbundesamt.de'
    option_list = BaseCommand.option_list + (
        make_option('--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Activate debugging'),
        make_option('--timeout',
            action='store',
            type=float,
            dest='timeout',
            default=1,
            help='Connection timeout in seconds, default is 1'),
        )

    URL = "http://www.umweltbundesamt.de/luftdaten/stations/locations?date=20150101" #dummy date param

    STATIONEN = {}

    def handle(self, *args, **options):
        self.options = options
        gevent.monkey.patch_socket()

        params = {}
        self.s = requests.Session()

        response = self.s.post(self.URL, params, timeout=self.options['timeout'])
        response.raise_for_status()

        reader = csv.DictReader(response.content.splitlines(), delimiter='\t')
        geolocator = Nominatim()

        for row in reader:
            address = geolocator.reverse((row['lat'], row['lon'])).raw['address']

            print address
            name = self.getStationName(row)
            position = self.getPosition(row)
            location = self.getLocationName(address)
            city = self.getCityName(address)
            amsl = self.getElevation(row)
            form_id = self.getFormId(row)
            slug = self.getSlug(row)

            MeasuringPoint.objects.update_or_create(
                name=name,
                defaults={
                    'name': name,
                    'position': position,
                    'location': location,
                    'city': city,
                    'amsl': amsl,
                    'form_id': form_id,
                    'slug': slug
                }
                )

    def getPosition(self, row):
        return Geoposition(Decimal(row['lat']), Decimal(Decimal(row['lon'])))

    def getElevation(self, row):
        return get_data().get_elevation(Decimal(row['lat']), Decimal(Decimal(row['lon'])))

    def getStationName(self, row):
        return HTMLParser().unescape(row['title'].rsplit(" ", 1)[0])

    def getLocationName(self, address):
        location = None
        if 'road' in address:
            location = address['road']
            if 'house_number' in address:
                location = location + ' ' + address['house_number']
        elif 'pedestrian' in address:
            location = address['pedestrian']
        elif 'path' in address:
            location = address['path']
        elif 'suburb' in address:
            location = address['suburb']
        else:
            location = address['farmyard']

        return location

    def getCityName(self, address):
        city = None
        if 'city' in address:
            city = address['city']
        elif 'town' in address:
            city = address['town']
        elif 'village' in address:
            city = address['village']
        else:
            city = address['state']

        return city

    def getFormId(self, row):
        return hash(row['stationCode']) & 0x7fffffff

    def getSlug(self, row):
        return row['stationCode']