from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view/(?P<slug>[^\.]+).xyz', views.view_post, name='view_blog_post'),
    url(r'^create_post/', views.create_post, name='create_post'),
    url(r'^create_category/', views.create_category, name='create_category'),
    url(r'^category/(?P<slug>[^\.]+).xyz', views.view_category, name='view_blog_category'),
]