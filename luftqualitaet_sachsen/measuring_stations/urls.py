# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers

from measuring_stations import views


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^$', views.overview, name='measuring_stations_measuringpoint_overview'),
    url(r'^station/(?P<slug>[-\w]+)/$', views.MeasuringPointDetailView.as_view(),
        name='measuring_stations_measuringpoint_detail'),
    url(r'^station/(?P<slug>[-\w]+)\.csv$', views.MeasuringPointCSVView.as_view(),
        name='measuring_stations_measuringpoint_csv'),
    url(r'^erklaerung/$', TemplateView.as_view(
        template_name='measuring_stations/explaination.html'), name='explaination')
]
