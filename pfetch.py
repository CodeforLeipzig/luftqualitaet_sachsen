#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import gevent.monkey
import requests
from bs4 import BeautifulSoup
from gevent.pool import Pool

gevent.monkey.patch_socket()

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


def fetchStation(params):
    response = requests.post(URL, params)
    soup = BeautifulSoup(response.text)
    params[VALIDATION_KEY] = soup.find_all(id=VALIDATION_KEY)[0]['value']
    params[VIEWSTATE_KEY] = soup.find_all(id=VIEWSTATE_KEY)[0]['value']
    schadstoffList = STATION_SCHADSTOFF_MAP[params[STATION_KEY]]
    schadstoffPool = Pool(len(schadstoffList))
    for schadstoff in schadstoffList:
        tmp = dict(params)
        tmp[SCHADSTOFF_KEY] = SCHADSTOFFE[schadstoff]
        tmp[TARGET_KEY] = SCHADSTOFF_KEY
        schadstoffPool.spawn(fetchSchadstoff, tmp)

    schadstoffPool.join()


def fetchSchadstoff(params):
        response = requests.post(URL, params)
        soup = BeautifulSoup(response.text)
        params[VALIDATION_KEY] = soup.find_all(id=VALIDATION_KEY)[0]['value']
        params[VIEWSTATE_KEY] = soup.find_all(id=VIEWSTATE_KEY)[0]['value']
        params[MITTELWERT_KEY] = MITTELWERT[MITTELWERT_SCHADSTOFF_MAP[params[SCHADSTOFF_KEY]]]
        params[ZEITRAUM_KEY] = 0
        params[TARGET_KEY] = MITTELWERT_KEY

        response = requests.post(URL, params)
        soup = BeautifulSoup(response.text)
        params[VALIDATION_KEY] = soup.find_all(id=VALIDATION_KEY)[0]['value']
        params[VIEWSTATE_KEY] = soup.find_all(id=VIEWSTATE_KEY)[0]['value']
        params[ZEITRAUM_KEY] = ZEITRAUM[sys.argv[1]]
        params[TARGET_KEY] = ZEITRAUM_KEY

        response = requests.post(URL, params)
        params[BUTTON_KEY] = BUTTON_VALUE
        soup = BeautifulSoup(response.text)
        params[VALIDATION_KEY] = soup.find_all(id=VALIDATION_KEY)[0]['value']
        params[VIEWSTATE_KEY] = soup.find_all(id=VIEWSTATE_KEY)[0]['value']
        del params[TARGET_KEY]
        response = requests.post(URL, params)

        if response.status_code == 200:
            with open(datetime.now().isoformat() + "_"
                      + params[STATION_KEY] + "_"
                      + params[SCHADSTOFF_KEY], 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)


if len(sys.argv) < 2 or not(sys.argv[1] in ZEITRAUM.keys()):
    print "Usage: fetch.py {24H|48H|7D|1M|3M|6M|1Y}"
    sys.exit(0)

stationPool = Pool(len(STATIONEN))
params = {}
response = requests.post(URL, params)
soup = BeautifulSoup(response.text)
params[VALIDATION_KEY] = soup.find_all(id=VALIDATION_KEY)[0]['value']
params[VIEWSTATE_KEY] = soup.find_all(id=VIEWSTATE_KEY)[0]['value']
params[TARGET_KEY] = STATION_KEY

for station in STATIONEN.keys():
    tmp = dict(params)
    tmp[STATION_KEY] = STATIONEN[station]
    stationPool.spawn(fetchStation, tmp)

stationPool.join()
