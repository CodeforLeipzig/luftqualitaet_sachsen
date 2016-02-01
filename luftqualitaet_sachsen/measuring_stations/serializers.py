# -*- coding: utf-8 -*-
from easy_thumbnails.exceptions import InvalidImageFormatError
from rest_framework import serializers
from . import models


class IndicatedValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatedValue


class MiniMeasuringPointSerializer(serializers.HyperlinkedModelSerializer):
    thumb = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    csv_url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='measuring_stations_measuringpoint_csv',
        lookup_field='slug'
    )

    class Meta:
        model = models.MeasuringPoint

    @staticmethod
    def get_category_display(obj):
        return obj.get_category_display()


    @staticmethod
    def get_thumb(obj):
        try:
            return obj.image['overview'].url
        except InvalidImageFormatError:
            pass


class MeasuringPointSerializer(serializers.ModelSerializer):
    indicated_values = serializers.SerializerMethodField()

    class Meta:
        model = models.MeasuringPoint

    @staticmethod
    def get_indicated_values(obj):
        serializer = IndicatedValueSerializer(obj.indicated_values.all()[:50], many=True)
        return serializer.data
