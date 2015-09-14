# -*- coding: utf-8 -*-
from rest_framework import serializers
from . import models


class MeasuringPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MeasuringPoint