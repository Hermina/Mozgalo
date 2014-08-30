from django.conf.urls import patterns, url

from dokumentacija import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^wiki', views.wiki, name='wiki'),
)
