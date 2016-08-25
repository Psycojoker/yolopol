# coding: utf-8

from django.db import models

from representatives_votes.models import Proposal

from .dossier_detail_base import DossierDetailBase


class DossierDetailProposals(DossierDetailBase):
    template_name = 'representatives_votes/dossier_detail_proposals.html'

    def get_context_data(self, **kwargs):
        c = super(DossierDetailProposals, self).get_context_data(**kwargs)

        c['tab'] = 'proposals'
        c['proposals'] = c['object'].proposals.filter(
            recommendation__isnull=True).prefetch_related('themes')

        return c
