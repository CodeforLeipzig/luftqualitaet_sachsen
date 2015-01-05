from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'luftqualitaet_sachsen.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('measuring_stations.urls')),
    url(r'^impressum/', TemplateView.as_view(template_name='impressum.html'), name='impressum')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
