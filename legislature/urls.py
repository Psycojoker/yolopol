# coding: utf-8
from __future__ import absolute_import

from django.conf.urls import url

from .views import group, representative

urlpatterns = [
    # List of groups by group kind
    url(
        r'^groups/(?P<kind>\w+)?$',
        group.index,
        name='group-index'
    ),
    # Representative detail by representative name
    url(
        r'^(?P<name>[-\w]+)$',
        representative.detail,
        name='representative-detail'
    ),
    # List of representatives by group kind and group name or pk
    url(
        r'^(?P<group_kind>\w+)/(?P<group>.+)$',
        representative.index,
        name='representative-index'
    ),
    # List all representatives by default
    url(
        r'',
        representative.index,
        name='representative-index'
    ),
]
