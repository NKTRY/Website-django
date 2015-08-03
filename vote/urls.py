from django.conf.urls import patterns, url

from vote.views import index, archive, vote, login, logout, change_password, register
from frontend.views import search

urlpatterns = patterns('',
    url(r'^$', index, name='vote_index'),
    url(r'^archive/$', archive, name='vote_archive'),
    url(r'^vote/(?P<question_id>\d+)/$', vote, name='vote_page'),
    url(r'^vote/(?P<question_id>\d+)/(?P<wechat_id>\w+)/$', vote, name='vote_page_tmp'),
    url(r'^login/$', login, name='vote_login'),
    url(r'^logout/$', logout, name='vote_logout'),
    url(r'^change-password/$', change_password, name='change_password'),
    url(r'^register/$', register, name='register'),
    url(r'^search/$', search, name="search"),
)
