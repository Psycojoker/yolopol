# Project specific "glue" coupling of all apps
from django.views import generic
from django.db import models

from core.views import GridListMixin, PaginationMixin
from representatives import views as representatives_views
from representatives.models import Representative
from representatives_votes import views as representatives_votes_views
from representatives_votes.models import Dossier
from representatives_positions.models import Position
from representatives_positions.forms import PositionForm
from representatives_recommendations.models import ScoredVote


class RepresentativeList(PaginationMixin, GridListMixin,
        representatives_views.RepresentativeList):
    pass


class RepresentativeDetail(representatives_views.RepresentativeDetail):
    queryset = Representative.objects.select_related('score')

    def get_queryset(self):
        qs = super(RepresentativeDetail, self).get_queryset()
        votes = ScoredVote.objects.select_related('proposal__recommendation')
        qs = qs.prefetch_related(models.Prefetch('votes', queryset=votes))
        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetail, self).get_context_data(**kwargs)
        c['position_form'] = PositionForm()
        self.add_representative_country_and_main_mandate(c['object'])
        return c


class PositionDetail(representatives_views.RepresentativeViewMixin,
        generic.DetailView):
    model = Position

    def get_queryset(self):
        qs = Position.objects.filter(published=True)
        qs = qs.select_related('representative__score')

        mandates = Mandate.objects.all().order_by(
            '-end_date').select_related('constituency__country', 'group')

        qs = qs.prefetch_related(
            models.Prefetch('representative__mandates', queryset=mandates))

        return qs


class DossierList(PaginationMixin, representatives_votes_views.DossierList):
    queryset = Dossier.objects.exclude(proposals__recommendation=None)
