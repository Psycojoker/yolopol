from dal import autocomplete

from django import forms

from .models import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Campaign
        widgets = {
            'dossiers': autocomplete.ModelSelect2Multiple(
                url='representatives_votes:dossier-autocomplete',
            )
        }
