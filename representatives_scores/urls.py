# coding: utf-8
from django.conf.urls import url

import views

urlpatterns = [
    url(
        r'^position/create/$',
        views.PositionCreate.as_view(),
        name='position-create'
    ),
    url(
        r'^position/(?P<pk>\d+)/$',
        views.PositionDetail.as_view(),
        name='position-detail'
    ),
    url(
        r'^representative/(?P<group_kind>\w+)/(?P<group>.+)/$',
        views.RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^representative/(?P<slug>[-\w]+)/$',
        views.RepresentativeDetail.as_view(),
        name='representative-detail'
    ),
    url(
        r'representative/',
        views.RepresentativeList.as_view(),
        name='representative-list'
    ),
    url(
        r'^groups/$',
        views.GroupList.as_view(),
        name='group-list'
    ),
    url(
        r'^groups/(?P<kind>\w+)/$',
        views.GroupList.as_view(),
        name='group-list'
    ),
    url(
        r'^dossier/(?P<pk>\d+)/$',
        views.DossierDetail.as_view(),
        name='dossier-detail'
    ),
    url(
        r'dossier/$',
        views.DossierList.as_view(),
        name='dossier-list'
    ),
]
