#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import sys
from cStringIO import StringIO

import gevent.monkey
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from django.core.management.base import BaseCommand
from gevent.pool import Pool

from ...models import IndicatedValue, MeasuringPoint


class Command(BaseCommand):
    args = '<period {24H|48H|7D|1M|3M|6M|1Y}>'
    help = 'Fetches data for the given period from www.umwelt.sachsen.de'
    URL = "http://www.umwelt.sachsen.de/umwelt/infosysteme/luftonline/Recherche.aspx"
    STATION_ID = "ctl00_Inhalt_StationList"
    STATION_KEY = "ctl00$Inhalt$StationList"
    SCHADSTOFF_ID = "ctl00_Inhalt_SchadstoffList"
    SCHADSTOFF_KEY = "ctl00$Inhalt$SchadstoffList"
    MITTELWERT_KEY = "ctl00$Inhalt$MwttList"
    ZEITRAUM_KEY = "ctl00$Inhalt$LetzteList"
    VALIDATION_KEY = "__EVENTVALIDATION"
    TARGET_KEY = "__EVENTTARGET"
    VIEWSTATE_KEY = "__VIEWSTATE"
    BUTTON_KEY = "ctl00$Inhalt$BtnCsvDown"
    BUTTON_VALUE = "CSV-Download"

    STATIONEN = {}
    SCHADSTOFFE = {
        "BEN": "161;1",
        "NO": "121;0",
        "NO2": "122;0",
        "O3": "23;0",
        "PM10": "224;0",
        "PM10_Pb": "560;2",
        "PM2.5": "109;2",
        "SO2": "22;1",
        "CO": "952;1",
    }

    MITTELWERT = {
        "STUNDEN": "45; 3600",
        "TAGE": "21; 86400",
        "MONATE": "177; 1",
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
    MITTELWERT_SCHADSTOFF_MAP = {
        "161;1": "STUNDEN",
        "121;0": "STUNDEN",
        "122;0": "STUNDEN",
        "23;0": "STUNDEN",
        "224;0": "TAGE",
        "109;2": "TAGE",
        "22;1": "STUNDEN",
        "560;2": "MONATE",
        "952;1": "STUNDEN",
    }

    headers = {}

    def handle(self, *args, **options):
        if len(args) < 1 or not(args[0] in self.ZEITRAUM.keys()):
            self.stdout.write("Usage: manage.py fetch {24H|48H|7D|1M|3M|6M|1Y}")
            sys.exit(0)

        gevent.monkey.patch_socket()

        params = {}
        self.s = requests.Session()

        response = self.s.post(self.URL, params, headers=self.headers)
        soup = BeautifulSoup(response.text)
        stations = soup.find(id=self.STATION_ID).find_all('option')
        for station in stations:
            self.STATIONEN[station.string] = station['value']
        params[self.VALIDATION_KEY] = soup.find(id=self.VALIDATION_KEY)['value']
        params[self.VIEWSTATE_KEY] = soup.find(id=self.VIEWSTATE_KEY)['value']
        params[self.TARGET_KEY] = self.STATION_KEY

        stationPool = Pool(len(self.STATIONEN))
        self.inv_stations = self.invert_dict(self.STATIONEN)
        self.inv_schadstoff = self.invert_dict(self.SCHADSTOFFE)
        #self.inv_schadstoff['109;2'] = 'PM2.5' # csv uses PM2.5

        for station in self.STATIONEN.keys():
            tmp = dict(params)
            tmp[self.STATION_KEY] = self.STATIONEN[station]
            stationPool.spawn(self.fetchStation, tmp, args[0])

        stationPool.join()

    def fetchStation(self, params, period):
        response = self.s.post(self.URL, params, headers=self.headers)
        soup = BeautifulSoup(response.text)

        params[self.VALIDATION_KEY] = soup.find(id=self.VALIDATION_KEY)['value']
        params[self.VIEWSTATE_KEY] = soup.find(id=self.VIEWSTATE_KEY)['value']
        schadstoffe = soup.find(id=self.SCHADSTOFF_ID).find_all('option')
        schadstoffList = []
        for schadstoff in schadstoffe:
            schadstoffList.append(schadstoff.text)
        schadstoffPool = Pool(len(schadstoffList))
        for schadstoff in schadstoffList:
            tmp = dict(params)
            tmp[self.SCHADSTOFF_KEY] = self.SCHADSTOFFE[schadstoff]
            tmp[self.TARGET_KEY] = self.SCHADSTOFF_KEY
            schadstoffPool.spawn(self.fetchSchadstoff, tmp, period)

        schadstoffPool.join()

    def fetchSchadstoff(self, params, period):
        response = self.s.post(self.URL, params, headers=self.headers)
        soup = BeautifulSoup(response.text)
        params[self.VALIDATION_KEY] = soup.find(id=self.VALIDATION_KEY)['value']
        params[self.VIEWSTATE_KEY] = soup.find(id=self.VIEWSTATE_KEY)['value']
        params[self.MITTELWERT_KEY] = self.MITTELWERT[
            self.MITTELWERT_SCHADSTOFF_MAP[params[self.SCHADSTOFF_KEY]]]
        params[self.ZEITRAUM_KEY] = 0
        params[self.TARGET_KEY] = self.MITTELWERT_KEY

        response = self.s.post(self.URL, params, headers=self.headers)
        soup = BeautifulSoup(response.text)

        params[self.VALIDATION_KEY] = soup.find(id=self.VALIDATION_KEY)['value']
        params[self.VIEWSTATE_KEY] = soup.find(id=self.VIEWSTATE_KEY)['value']
        params[self.ZEITRAUM_KEY] = self.ZEITRAUM[period]
        params[self.TARGET_KEY] = self.ZEITRAUM_KEY

        response = self.s.post(self.URL, params, headers=self.headers)
        soup = BeautifulSoup(response.text)

        params[self.BUTTON_KEY] = self.BUTTON_VALUE
        params[self.VALIDATION_KEY] = soup.find(id=self.VALIDATION_KEY)['value']
        params[self.VIEWSTATE_KEY] = soup.find(id=self.VIEWSTATE_KEY)['value']
        del params[self.TARGET_KEY]

        response = self.s.post(self.URL, params, headers=self.headers)

        if response.status_code == 200:
            f = StringIO(response.content)
            reader = csv.DictReader(f, delimiter=';')
            stationName = self.inv_stations[params[self.STATION_KEY]]
            print stationName
            station = MeasuringPoint.objects.get(name=stationName)
            unit = self.inv_schadstoff[params[self.SCHADSTOFF_KEY]]
            for row in reader:
                dateRow = row['Datum Zeit']
                if len(dateRow) > 0:
                    try:
                        date = parser.parse(dateRow)
                    except ValueError:
                        continue
                    value = row[(' ' + stationName + ' ' + unit).encode('iso-8859-1')].strip()

                    if value.find(',') > -1:
                        value = float(value.replace(",","."))
                        
                    if (isinstance(value, float) or (value.find('g/m') == -1 and value.find('n. def.') == -1)):
                        IndicatedValue.objects.update_or_create(date_created=date,
                                    measuring_point=station, defaults={unit.lower(): float(value)})
            f.close

    def invert_dict(self, d):
        return dict([(v, k) for k, v in d.iteritems()])
