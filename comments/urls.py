from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^post/$', views.post, name='index'),
    url(r'^fetch/$', views.fetch_all, name='list_all'),
]