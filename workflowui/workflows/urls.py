from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.submit, name='new'),
    url(r'^save/(?P<pk>\d+)/$', views.submit, name='save'),
    url(r'^submit/(?P<pk>\d+)/$', views.submit, name='submit'),
    url(r'^monitor/(?P<pk>\d+)/$', views.monitor, name='monitor'),
]
