from django.conf.urls import patterns, url, include
from jsonrpc.backend.django import api

urlpatterns = patterns(
    '',
    url(r'', include(api.urls)),
    url(r'prefix', include(api.urls)),
)
