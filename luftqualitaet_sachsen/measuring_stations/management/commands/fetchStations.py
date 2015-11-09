#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

import gevent.monkey
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from optparse import make_option
from HTMLParser import HTMLParser

from srtm import get_data
from geoposition.fields import Geoposition
from geopy.geocoders import Nominatim
from gevent.pool import Pool
from decimal import Decimal
from progressbar import ProgressBar, Percentage, Bar

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

    POLLUTANTS = {
        "NO2": "NO2",
        "O3": "O3",
        "PM10": "PM1",
        "SO2": "SO2",
        "CO": "CO",
    }

    AVERAGE_POLLUTANT_MAP = {
        "NO2": "1SMW",
        "O3": "1SMW",
        "PM10": "1TMW",
        "SO2": "1SMW",
        "CO": "8SMW",
    }

    POLLUTANTS_FIELD_MAP = {
        "NO2": "no2",
        "O3": "o3",
        "PM10": "pm10",
        "SO2": "so2",
        "CO": "co",
    }

    def handle(self, *args, **options):
        self.options = options
        gevent.monkey.patch_socket()

        self.s = requests.Session()

        #pollutantPool = Pool(len(self.POLLUTANTS))
        pollutantPool = Pool(1)

        for pollutant in self.POLLUTANTS:
            pollutantPool.spawn(self.fetchStations, pollutant)

        pollutantPool.join()

    def fetchStations(self, pollutant):
        params = {}
        params['pollutant'] = self.POLLUTANTS[pollutant]
        params['data_type'] = self.AVERAGE_POLLUTANT_MAP[pollutant]

        response = self.s.post(self.URL, params, timeout=self.options['timeout'])
        response.raise_for_status()

        lines = response.content.splitlines()
        reader = csv.DictReader(lines, delimiter='\t')
        geolocator = Nominatim()
        pbar = ProgressBar(widgets=[pollutant + ': ', Percentage(), Bar()], maxval=len(lines)).start()
        i = 0

        for row in reader:
            defaults = {}
            defaults['name'] = self.getStationName(row)
            defaults['position'] = self.getPosition(row)
            defaults['amsl'] = self.getElevation(row)
            defaults['form_id'] = self.getFormId(row)
            defaults['slug'] = self.getSlug(row)

            with transaction.atomic():
                entry = MeasuringPoint.objects.select_for_update().filter(name=defaults['name']).last()

                if (entry == None):
                    entries = MeasuringPoint.objects.select_for_update().filter(slug=defaults['slug']).last()

                    if (entry == None):
                        address = geolocator.reverse((row['lat'], row['lon'])).raw['address']
                        defaults['location'] = self.getLocationName(address)
                        defaults['city'] = self.getCityName(address)
                        defaults[self.POLLUTANTS_FIELD_MAP[pollutant]] = True
                        MeasuringPoint.objects.create(**defaults)
                    else:
                        entry[self.POLLUTANTS_FIELD_MAP[pollutant]] = True
                        entry.save()

                else:
                    setattr(entry, self.POLLUTANTS_FIELD_MAP[pollutant], True)
                    entry.save()

            pbar.update(i)
            i = i + 1

        pbar.finish()

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
        elif 'farmyard' in address:
            location = address['farmyard']
        else:
            location = address['footway']

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