from django.conf.urls import url

from .views import Blogs


urlpatterns = [
    url(r'^blogs/$', Blogs.as_view(), name='index'),
]