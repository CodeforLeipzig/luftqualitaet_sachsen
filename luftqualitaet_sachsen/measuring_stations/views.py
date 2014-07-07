from django.views.generic import TemplateView
from django.shortcuts import render
from .models import MeasuringPoint


def overview(request):
    ctx = {'measuring_points': MeasuringPoint.objects.all()}
    return render(request, "measuring_stations/home.html", ctx)
