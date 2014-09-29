# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import IndicatedValue, MeasuringPoint


class IndicatedValueAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('measuring_point',) + IndicatedValue.csv_fields
    list_display_links = ('date_created',)
    list_filter = ('measuring_point',)


class MeasuringPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'city', 'amsl', 'eu_typing', 'category')
    list_filter = ('city', 'eu_typing', 'category')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'location']


admin.site.register(IndicatedValue, IndicatedValueAdmin)
admin.site.register(MeasuringPoint, MeasuringPointAdmin)
