from django.http import HttpResponse
from django.views.generic import DetailView
from django.shortcuts import render
from geopy import distance
from rest_framework import viewsets
from rest_framework.response import Response

from .models import MeasuringPoint
from. import serializers


def overview(request):
    ctx = {'measuring_points': MeasuringPoint.objects.all()}
    return render(request, 'measuring_stations/overview.html', ctx)


class MeasuringPointDetailView(DetailView):
    model = MeasuringPoint

    def nearest_stations(self):
        results = []
        for station in self.model.objects.exclude(slug=self.object.slug):
            d = distance.distance(
                (self.object.position.latitude, self.object.position.longitude),
                (station.position.latitude, station.position.longitude)
            )
            results.append({'distance': d, 'obj': station})
        results = sorted(results, key=lambda k: k['distance'])
        return results[:5]


class MeasuringPointCSVView(DetailView):
    model = MeasuringPoint

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.object.slug

        return self.object.get_csv(response, self.request.GET.get('limit', 50),
            bool(int(self.request.GET.get('flat', 0))))


class MeasuringPointView(viewsets.ReadOnlyModelViewSet):
    queryset = MeasuringPoint.objects.all()

    def list(self, request):
        qs = self.get_queryset()
        serializer = serializers.MiniMeasuringPointSerializer(
            qs, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        qs = self.get_queryset().filter(pk=pk).prefetch_related('indicated_values').last()
        serializer = serializers.MeasuringPointSerializer(qs, context={'request': request})
        return Response(serializer.data)
