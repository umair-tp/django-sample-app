from django.conf.urls import url
from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token, verify_jwt_token

from . import views


urlpatterns = [
    url(r'^auth-jwt/', obtain_jwt_token),
    url(r'^auth-jwt-refresh/', refresh_jwt_token),
    url(r'^auth-jwt-verify/', verify_jwt_token),
    url(r'^api/',
        include([
            url(r'^photos/$', views.photos_list),
            url(r'^$', views.PhotoCreateReadView.as_view(), name="photo_rest_api"),
            url(r'^(?P<id>[-\d]+)/$', views.PhotoReadUpdateDeleteView.as_view(), name="photo_rest_api")
        ])),
    path('', views.index, name='index'),
]