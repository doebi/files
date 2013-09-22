from django.conf.urls import patterns, url
from cryptainer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<name>\w+)/$', views.folder, name='folder'),
    url(r'^(?P<folder>\w+)/(?P<name>\w+)/$', views.get, name='get'),
)
