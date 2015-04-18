from django.conf.urls import patterns, include, url
from appbucket.views import *

urlpatterns = patterns('',
    url(r'^index$', index, name="index"),
)