from django.conf.urls import url, include
from django.contrib import admin
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process/(?P<action>\w+)$', views.process),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success)
]