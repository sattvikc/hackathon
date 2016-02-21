from django.conf.urls import url

from . import views

urlpatterns = [
    # Workflow stuff
    url(r'^$', views.wlist, name='list'),
    url(r'^new/$', views.submit, name='new'),
    url(r'^save/(?P<pk>\d+)/$', views.submit, name='save'),
    url(r'^execute/(?P<pk>\d+)/$', views.execute, name='execute'),
    url(r'^submit/(?P<pk>\d+)/$', views.submit, name='submit'),

    # Monitoring stuff
    url(r'^monitor/$', views.mlist, name='mlist'),
    url(r'^monitor/(?P<pk>\d+)/$', views.monitor, name='monitor'),
]
