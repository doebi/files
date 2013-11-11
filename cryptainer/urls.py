from django.conf.urls import patterns, url
from cryptainer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^token/$', views.token, name='token'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^(?P<name>\w+)/$', views.folder, name='folder'),
    url(r'^(?P<folder>\w+)/(?P<name>\w+)/$', views.get, name='get'),
    url(r'^(?P<folder>\w+)/(?P<name>\w+)/tn$', views.thumbnail, name='thumbnail'),
)
