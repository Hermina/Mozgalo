from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^podaci/', include('podaci.urls')),
    url(r'^$', include('podaci.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dokumentacija/', include('dokumentacija.urls')),
)
