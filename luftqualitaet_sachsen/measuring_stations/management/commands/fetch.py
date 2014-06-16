#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import gevent.monkey
import requests
from bs4 import BeautifulSoup
from gevent.pool import Pool

from django.core.management.base import BaseCommand

from cStringIO import StringIO


class Command(BaseCommand):
    args = '<period {24H|48H|7D|1M|3M|6M|1Y}>'
    help = 'Fetches data for the given period from www.umwelt.sachsen.de'
    URL = "http://www.umwelt.sachsen.de/umwelt/infosysteme/luftonline/Recherche.aspx"
    STATION_KEY = "ctl00$Inhalt$StationList"
    SCHADSTOFF_KEY = "ctl00$Inhalt$SchadstoffList"
    MITTELWERT_KEY = "ctl00$Inhalt$MwttList"
    ZEITRAUM_KEY = "ctl00$Inhalt$LetzteList"
    VALIDATION_KEY = "__EVENTVALIDATION"
    TARGET_KEY = "__EVENTTARGET"
    VIEWSTATE_KEY = "__VIEWSTATE"
    BUTTON_KEY = "ctl00$Inhalt$BtnCsvDown"
    BUTTON_VALUE = "CSV-Download"

    STATIONEN = {
        "Leipzig-Luetzner Straße": "224",
        "Leipzig-Mitte": "211",
        "Leipzig-Thekla": "214",
        "Leipzig-West": "213"
    }
    SCHADSTOFFE = {
        "BEN": "161;1",
        "NO": "121;0",
        "NO2": "122;0",
        "O3": "23;0",
        "PM10": "224;0",
        "PM25": "109;2",
        "SO2": "22;1"
    }
    MITTELWERT = {
        "STUNDEN": "15; 3600",
        "TAGE": "21; 86400"
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
    STATION_SCHADSTOFF_MAP = {
        "224": ["NO", "NO2", "PM10", "PM25"],
        "211": ["BEN", "NO", "NO2", "O3", "PM10", "PM25", "SO2"],
        "214": ["O3"],
        "213": ["BEN", "NO", "NO2", "O3", "PM10", "PM25", "SO2"]
    }
    MITTELWERT_SCHADSTOFF_MAP = {
        "161;1": "STUNDEN",
        "121;0": "STUNDEN",
        "122;0": "STUNDEN",
        "23;0": "STUNDEN",
        "224;0": "TAGE",
        "109;2": "TAGE",
        "22;1": "STUNDEN"
    }

    def handle(self, *args, **options):
        if len(args) < 1 or not(args[0] in self.ZEITRAUM.keys()):
            self.stdout.write("Usage: manage.py fetch {24H|48H|7D|1M|3M|6M|1Y}")
            sys.exit(0)

        gevent.monkey.patch_socket()

        stationPool = Pool(len(self.STATIONEN))
        params = {}
        response = requests.post(self.URL, params)
        soup = BeautifulSoup(response.text)
        params[self.VALIDATION_KEY] = soup.find_all(id=self.VALIDATION_KEY)[0]['value']
        params[self.VIEWSTATE_KEY] = soup.find_all(id=self.VIEWSTATE_KEY)[0]['value']
        params[self.TARGET_KEY] = self.STATION_KEY

        for station in self.STATIONEN.keys():
            tmp = dict(params)
            tmp[self.STATION_KEY] = self.STATIONEN[station]
            stationPool.spawn(self.fetchStation, tmp, args[0])

        stationPool.join()

    def fetchStation(self, params, period):
        response = requests.post(self.URL, params)
        soup = BeautifulSoup(response.text)
        params[self.VALIDATION_KEY] = soup.find_all(id=self.VALIDATION_KEY)[0]['value']
        params[self.VIEWSTATE_KEY] = soup.find_all(id=self.VIEWSTATE_KEY)[0]['value']
        schadstoffList = self.STATION_SCHADSTOFF_MAP[params[self.STATION_KEY]]
        schadstoffPool = Pool(len(schadstoffList))
        for schadstoff in schadstoffList:
            tmp = dict(params)
            tmp[self.SCHADSTOFF_KEY] = self.SCHADSTOFFE[schadstoff]
            tmp[self.TARGET_KEY] = self.SCHADSTOFF_KEY
            schadstoffPool.spawn(self.fetchSchadstoff, tmp, period)

        schadstoffPool.join()

    def fetchSchadstoff(self, params, period):
            response = requests.post(self.URL, params)
            soup = BeautifulSoup(response.text)
            params[self.VALIDATION_KEY] = soup.find_all(id=self.VALIDATION_KEY)[0]['value']
            params[self.VIEWSTATE_KEY] = soup.find_all(id=self.VIEWSTATE_KEY)[0]['value']
            params[self.MITTELWERT_KEY] = self.MITTELWERT[
                self.MITTELWERT_SCHADSTOFF_MAP[params[self.SCHADSTOFF_KEY]]]
            params[self.ZEITRAUM_KEY] = 0
            params[self.TARGET_KEY] = self.MITTELWERT_KEY

            response = requests.post(self.URL, params)
            soup = BeautifulSoup(response.text)
            params[self.VALIDATION_KEY] = soup.find_all(id=self.VALIDATION_KEY)[0]['value']
            params[self.VIEWSTATE_KEY] = soup.find_all(id=self.VIEWSTATE_KEY)[0]['value']
            params[self.ZEITRAUM_KEY] = self.ZEITRAUM[period]
            params[self.TARGET_KEY] = self.ZEITRAUM_KEY

            response = requests.post(self.URL, params)
            params[self.BUTTON_KEY] = self.BUTTON_VALUE
            soup = BeautifulSoup(response.text)
            params[self.VALIDATION_KEY] = soup.find_all(id=self.VALIDATION_KEY)[0]['value']
            params[self.VIEWSTATE_KEY] = soup.find_all(id=self.VIEWSTATE_KEY)[0]['value']
            del params[self.TARGET_KEY]
            response = requests.post(self.URL, params)

            if response.status_code == 200:
                f = StringIO()
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                f.close