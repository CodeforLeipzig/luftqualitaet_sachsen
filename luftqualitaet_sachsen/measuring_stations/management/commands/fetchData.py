#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

import gevent.monkey
import requests
import json
from dateutil import parser
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from gevent.pool import Pool
from optparse import make_option
from pytz.exceptions import NonExistentTimeError
from requests import exceptions
from progressbar import ProgressBar, Percentage, Bar

from ...models import IndicatedValue, MeasuringPoint


class Command(BaseCommand):
    args = '<period {24H|48H|7D|1M|3M|6M|1Y}>'
    help = 'Fetches data for the given period from www.umweltbundesamt.de'
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

    URL = "http://www.umweltbundesamt.de/luftdaten/data"

    STATIONEN = {}

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

    ZEITRAUM = {
        "24H": "1",
        "48H": "2",
        "7D": "3",
        "1M": "4",
        "3M": "5",
        "6M": "6",
        "1Y": "7"
    }

    YEAR_MONTH_DAY = '%Y%m%d'

    headers = {}
    params = {}

    def handle(self, *args, **options):
        if len(args) < 1 or not(args[0] in self.ZEITRAUM.keys()):
            self.stdout.write("Usage: manage.py fetch-data {24H|48H|7D|1M|3M|6M|1Y}")
            sys.exit(0)
        self.options = options
        gevent.monkey.patch_socket()

        self.s = requests.Session()
        self.tz = timezone.get_current_timezone()
        stations = MeasuringPoint.objects.all()

        #stationPool = Pool(len(stations))
        stationPool = Pool(1)
        self.inv_pollutants = self.invert_dict(self.POLLUTANTS)

        today = date.today()
        dateRange = self.getDateRange(args[0])
        self.params['dateTo'] = today.strftime(self.YEAR_MONTH_DAY)
        self.params['date'] = (today - dateRange).strftime(self.YEAR_MONTH_DAY)
        pbar = ProgressBar(widgets=['Lade Daten' + ': ', Percentage(), Bar()], maxval=len(stations)).start()
        j = 0
        for station in stations:
            stationPool.spawn(self.fetchStation, station.slug)
            pbar.update(j)
            j = j + 1

        stationPool.join()

    def fetchStation(self, stationId):
            #pollutantPool = Pool(len(self.POLLUTANTS))
            pollutantPool = Pool(1)

            for pollutant in self.POLLUTANTS:
                pollutantPool.spawn(self.fetchPollutant, stationId, pollutant)

            pollutantPool.join()

    def get(self, params):
        response = None
        params.update(self.params)
        try:
            response = self.s.get(self.URL, params=params, timeout=self.options['timeout'])
            response.raise_for_status()
        except (exceptions.ConnectionError, exceptions.HTTPError) as e:
            self.stderr.write(str(e))
            if self.options['debug']:
                self.stderr.write('{url}\n{body}'.format(url=response.request.url,
                    body=response.request.body.replace('&', '\n')))
        return response

    def fetchPollutant(self, stationId, pollutant):
        params = {}
        params.update(self.params)
        params['station'] = stationId
        params['pollutant'] = self.POLLUTANTS[pollutant]
        params['data_type'] = self.AVERAGE_POLLUTANT_MAP[pollutant]
        response = self.get(params)

        if response and response.status_code == 200:
            try:
                station = MeasuringPoint.objects.get(slug=stationId)
            except MeasuringPoint.DoesNotExist:
                self.stderr.write(u'MeasuringPoint "{0}"" not found'.format(station))
                return

            unit = self.inv_pollutants[self.POLLUTANTS[pollutant]]
            unit_key = unit.lower().replace('.', '')
            data = json.loads(response.content)
            values = data['values']

            if values:
                for dateKey, valueList in values.items():
                    if len(valueList):
                        i = -1
                        for value in valueList:
                            i = i + 1
                            try:
                                date = parser.parse(dateKey, dayfirst=True)
                                if timezone.is_naive(date):
                                    try:
                                        date = timezone.make_aware(date, self.tz)
                                    except NonExistentTimeError as e:
                                        self.stderr.write(str(e))
                                date = date + timedelta(hours=i)
                            except ValueError:
                                self.stderr.write('Failed to parse date "{0}"'.format(date))
                                continue

                            value = value.replace(',', '.')
                            value = float(value)

                            if value != -999.0:
                                IndicatedValue.objects.update_or_create(date_created=date,
                                            measuring_point=station, defaults={unit_key: value})

    @classmethod
    def invert_dict(cls, d):
        return dict([(v, k) for k, v in d.iteritems()])

    @classmethod
    def getDateRange(cls, range):
        if (range == '24H'):
            return timedelta(days=1)
        elif  (range == '48H'):
            return timedelta(days=2)
        elif  (range == '7D'):
            return timedelta(days=7)
        elif  (range == '1M'):
            return timedelta(days=31)
        elif  (range == '3M'):
            return timedelta(days=92)
        elif  (range == '6M'):
            return timedelta(days=184)
        elif  (range == '1Y'):
            return timedelta(days=366)