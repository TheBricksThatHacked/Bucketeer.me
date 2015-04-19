from django.conf.urls import patterns, include, url
from django.contrib import admin
from appbucket.urls import urlpatterns as appbucket_urls
from django.conf import settings
from django.conf.urls.static import static
from appbucket.ajax import urlpatterns as ajax_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bucket.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(appbucket_urls, namespace="app")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/$', 'bucket.views.register', name='register'),
    url(r'^ajax/', include(ajax_urls, namespace="ajax")),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

