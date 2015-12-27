from django.views import generic

from .models import Position
from .forms import PositionForm


class PositionCreate(generic.CreateView):
    model = Position
    fields = PositionForm.Meta.fields + ['representative']

    def get_success_url(self):
        return self.object.representative.get_absolute_url()


class PositionDetail(generic.DetailView):
    model = Position
