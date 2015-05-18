# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class MeasuringPointManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)
