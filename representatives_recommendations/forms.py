from django import forms


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['recommendation', 'title', 'description', 'weight']
