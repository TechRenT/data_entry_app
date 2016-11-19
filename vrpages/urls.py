from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.vrpage_list),
    url(r'(?P<vrpage_pk>\d+)/(?P<rawurl_pk>\d+)/$', views.rawurl_detail),
    url(r'(?P<pk>\d+)/$', views.vrpage_detail),
]