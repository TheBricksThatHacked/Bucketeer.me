from django.conf.urls import patterns, include, url
from django.contrib import admin
from appbucket.urls import urlpatterns as appbucket_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bucket.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^bucket/', include(appbucket_urls, namespace="app")),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/$', 'bucket.views.register', name='register'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

