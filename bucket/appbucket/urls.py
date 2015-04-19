from django.conf.urls import patterns, include, url
from appbucket.views import *

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^profile/(?P<user_id>\d+)/$', 'appbucket.views.user_profile', name='user_profile'),
    url(r'^profile/edit/$', 'appbucket.views.edit_profile', name='edit_profile'),
    
)
