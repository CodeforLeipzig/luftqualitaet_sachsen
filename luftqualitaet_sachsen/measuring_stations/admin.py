# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import IndicatedValue, MeasuringPoint


class MeasuringPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'amsl', 'eu_typing', 'category')
    list_filter = ('eu_typing', 'category')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'location']


admin.site.register(IndicatedValue)
admin.site.register(MeasuringPoint, MeasuringPointAdmin)
