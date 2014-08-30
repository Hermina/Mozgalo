from django.conf.urls import patterns, url

from podaci import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^update/$', views.update, name='update'),
    url(r'^full_update/$', views.full_update, name='full_update'),
    url(r'^analiza/$', views.analysis_index, name='analiza'),
    url(r'^ciljano/$', views.manually, name='ciljano'),
    url(r'^spremi/$', views.storing, name='spremi'),
    url(r'^recommender/$', views.recommender, name='recommender'),
    url(r'^recommender_result/$', views.recommender_result, name='recommender_result'),
    url(r'^analysis_google/$', views.analysis_google_map, name='analysis_google'),
    url(r'^analysis_vs/$', views.analysis_vs, name='analysis_vs'),
    url(r'^analysis_vs_result/$', views.analysis_vs_result, name='analysis_vs_result'),
    url(r'^analysis_basic/$', views.analysis_basic, name='analysis_basic'),
)
