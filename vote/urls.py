from django.conf.urls import patterns, url

from .views import index, archive, vote, login, logout, change_password

urlpatterns = patterns('',
    url(r'^$', index, name='vote_index'),
    url(r'^archive/$', archive, name='vote_archive'),
    url(r'^$', vote, name='vote_page')
)
