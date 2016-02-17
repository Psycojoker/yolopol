# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.views import generic

import views
import api

admin.autodiscover()

urlpatterns = [
    # Project-specific overrides
    url(
        r'^legislature/representative/(?P<group_kind>\w+)/(?P<group>.+)/$',
        views.RepresentativeList.as_view(),
    ),
    url(
        r'^legislature/representative/(?P<slug>[-\w]+)/$',
        views.RepresentativeDetail.as_view(),
    ),
    url(
        r'^legislature/representative/$',
        views.RepresentativeList.as_view(),
    ),
    url(
        r'^votes/dossier/$',
        views.DossierList.as_view(),
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rq/', include('django_rq.urls')),
    url(r'^legislature/', include('representatives.urls',
        namespace='representatives')),
    url(r'^votes/', include('representatives_votes.urls',
        namespace='representatives_votes')),
    url(r'^positions/', include('representatives_positions.urls',
        namespace='representatives_positions')),
    url(r'^api/', include(api.router.urls)),
    url(r'^$', generic.TemplateView.as_view(template_name='home.html')),
]
