from django.views import generic

from .models import Campaign


class CampaignListView(generic.ListView):
    model = Campaign


class CampaignDetailView(generic.DetailView):
    model = Campaign
