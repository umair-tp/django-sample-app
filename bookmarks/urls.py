from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^create/$', views.index, name='index'),
    url(r'^$', views.list_all, name='list_all'),
]