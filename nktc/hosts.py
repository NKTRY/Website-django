from django_hosts import patterns, host

from accounts.admin import superadminsite, normaladminsite


host_patterns = patterns('',
    host(r'www.test', 'frontend.urls', name='www'),
    host(r'test', 'frontend.urls', name='default'),
    host(r'admin.test', 'accounts.surls', name='normal'),
    host(r'nktc.test', 'accounts.nurls', name='super')
)