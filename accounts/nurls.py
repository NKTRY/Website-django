from django.conf.urls import patterns, include, url
from django.contrib import admin

from accounts.admin import normaladminsite


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nktc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(normaladminsite.urls)),
)