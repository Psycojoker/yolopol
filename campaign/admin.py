from django.contrib import admin

from .forms import CampaignForm
from .models import Campaign


class CampaignAdmin(admin.ModelAdmin):
    form = CampaignForm
admin.site.register(Campaign, CampaignAdmin)
