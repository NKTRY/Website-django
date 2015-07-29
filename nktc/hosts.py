from django_hosts import patterns, host


host_patterns = patterns('',
    host(r'www', 'frontend.urls', name='www'),
    host(r'', 'frontend.urls', name='default'),
    host(r'admin', 'accounts.nurls', name='normal'),
    host(r'nktc', 'accounts.surls', name='super'),
    host(r'werobot', 'wechat.urls', name='werobot'),
    host(r'vote', 'vote.urls', name='vote')
)