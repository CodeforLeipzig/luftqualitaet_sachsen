# -*- coding: utf-8 -*-
from django.conf.urls import url

from measuring_stations import views


urlpatterns = [
    url(r'^$', views.overview, name='measuring_stations_measuringpoint_home'),
]
