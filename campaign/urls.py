from django.conf.urls import url

import views

urlpatterns = [
    url(
        r'^$',
        views.CampaignListView.as_view(),
        name='campaign-list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.CampaignDetailView.as_view(),
        name='campaign-detail'
    ),
]
