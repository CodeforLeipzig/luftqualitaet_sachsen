# -*- coding: utf-8 -*-
from rest_framework import serializers
from . import models


class IndicatedValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatedValue


class MiniMeasuringPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MeasuringPoint


class MeasuringPointSerializer(serializers.ModelSerializer):
    indicated_values = serializers.SerializerMethodField()

    class Meta:
        model = models.MeasuringPoint

    def get_indicated_values(self, obj):
        serializer = IndicatedValueSerializer(obj.indicated_values.all()[:50], many=True)
        return serializer.data