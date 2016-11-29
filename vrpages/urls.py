from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^qualify/$', views.vrpage_qualify_list, name='qualify_list'),
    url(r'^polish/$', views.vrpage_polish_list, name='polish_list'),
    url(r'^qualify_polish/$', views.qualify_polish_list, name='qualify_polish_list'),
    url(r'^(?P<pk>\d+)/qualify/$', views.rawurl_qualify, name='rawurl_qualify'),
    url(r'^(?P<pk>\d+)/polish/$', views.rawurl_polish, name='rawurl_polish'),
    url(r'^(?P<pk>\d+)/qualify_polish/$', views.qualify_polish, name='qualify_polish'),
    # url(r'^(?P<pk>\d+)/assign_rawurls/$', views.assign_rawurls, name='assign_rawurls'),
    url(r'^(?P<pk>\d+)/no_task/$', views.no_task, name='no_task'),
]