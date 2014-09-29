from django.http import HttpResponse
from django.views.generic import DetailView
from django.shortcuts import render

from .models import MeasuringPoint


def overview(request):
    ctx = {'measuring_points': MeasuringPoint.objects.all()}
    return render(request, 'measuring_stations/overview.html', ctx)


class MeasuringPointDetailView(DetailView):
    model = MeasuringPoint


class MeasuringPointCSVView(DetailView):
    model = MeasuringPoint

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.object.slug
        return self.object.get_csv(response)
