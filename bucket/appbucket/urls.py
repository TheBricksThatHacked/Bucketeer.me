from django.conf.urls import patterns, include, url
from appbucket.views import *

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^about/$', 'appbucket.views.about', name='about'),
    url(r'^badges/$', 'appbucket.views.badges', name='badges'),
    url(r'^profile/$', 'appbucket.views.my_profile', name='my_profile'),
    url(r'^profile/id/(?P<user_id>\d+)/$', 'appbucket.views.user_profile', name='user_profile'),
    url(r'^profile/edit/$', 'appbucket.views.edit_profile', name='edit_profile'),
    url(r'^profile/(?P<user_name>[a-zA-Z0-9.-]+)/$', 'appbucket.views.user_profile', name='user_profile_name'),
    url(r'^addItem/$', 'appbucket.views.add_item', name='add_item'),
    url(r'^item/edit/(?P<item_id>\d+)/$', 'appbucket.views.edit_item', name='edit_item'),
    
)

