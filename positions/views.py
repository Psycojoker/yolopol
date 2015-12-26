# coding: utf-8
from __future__ import absolute_import

from datetime import datetime

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.views import generic
from django import http
from django import shortcuts
from django.db import models
from django.utils.text import slugify

from representatives.models import Group
from representatives_votes.models import Dossier

from .forms import PositionForm
from .models import Position, PositionsRepresentative, PositionsVote


class PaginationMixin(object):
    pagination_limits = (12, 24, 48, 96)

    def get_paginate_by(self, queryset):
        if 'paginate_by' in self.request.GET:
            self.request.session['paginate_by'] = \
                unicode(self.request.GET['paginate_by'])

        elif 'paginate_by' not in self.request.session:
            self.request.session['paginate_by'] = 12
        return self.request.session['paginate_by']

    def get_context_data(self, **kwargs):
        c = super(PaginationMixin, self).get_context_data(**kwargs)
        c['pagination_limits'] = self.pagination_limits
        return c


class RepresentativeList(PaginationMixin, generic.ListView):
    def set_session_display(self):
        if self.request.GET.get('display') in ('grid', 'list'):
            self.request.session['display'] = self.request.GET.get('display')

        if 'display' not in self.request.session:
            self.request.session['display'] = 'grid'

    def get(self, *args, **kwargs):
        self.set_session_display()
        return super(RepresentativeList, self).get(*args, **kwargs)

    def get_template_names(self):
        return [
            'positions/representative_{}.html'.format(
                self.request.session['display'])
        ]

    def search_filter(self, qs):
        search = self.request.GET.get('search', None)
        if search:
            qs = qs.filter(slug__icontains=slugify(search))
        return qs

    def group_filter(self, qs):
        group_kind = self.kwargs.get('group_kind', None)
        group = self.kwargs.get('group', None)

        if group_kind and group:
            if group.isnumeric():
                # Search group based on pk
                qs = qs.filter(
                    mandates__group_id=int(group),
                    mandates__end_date__gte=datetime.now()
                )
            else:
                # Search group based on abbreviation
                qs = qs.filter(
                    models.Q(mandates__group__abbreviation=group),
                    mandates__group__kind=group_kind,
                    mandates__end_date__gte=datetime.now()
                )
        return qs

    def fetch_relations(self, qs):
        qs = qs.select_related('votes_profile')
        qs = PositionsRepresentative.objects.prefetch_profile(qs)
        return qs

    def get_queryset(self):
        qs = PositionsRepresentative.objects.filter(active=True)
        qs = self.group_filter(qs)
        qs = self.search_filter(qs)
        qs = self.fetch_relations(qs)
        return qs


class RepresentativeDetail(generic.DetailView):
    template_name = 'positions/representative_detail.html'
    context_object_name = 'representative'

    def get_queryset(request):
        qs = PositionsRepresentative.objects.select_related('votes_profile')
        qs = PositionsRepresentative.objects.prefetch_profile(qs)
        qs = PositionsRepresentative.objects.prefetch_votes(qs)
        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetail, self).get_context_data(**kwargs)

        c['votes'] = c['object'].votes.all()
        c['mandates'] = c['object'].mandates.all()
        c['positions'] = c['object'].positions.filter(published=True
            ).prefetch_related('tags')

        c['position_form'] = PositionForm()

        return c


class DossierList(PaginationMixin, generic.ListView):
    def dossier_index(request):
        dossier_list = Dossier.objects.all()

        return render_paginate_list(
            request,
            dossier_list,
            'votes/dossier_index.html'
        )


class DossierDetail(PaginationMixin, generic.DetailView):
    def dossier_detail(request, pk):
        dossier = get_object_or_404(Dossier, pk=pk)

        return render(
            request,
            'votes/dossier_detail.html',
            {'dossier': dossier}
        )


class GroupList(generic.ListView):
    def group_index(request, kind=None):
        groups = Group.objects.filter(
            mandates__end_date__gte=datetime.now()
        )

        if kind:
            groups = groups.filter(
                kind=kind
            )

        groups = groups.distinct().order_by('name')
        return render(
            request,
            'legislature/groups_list.html',
            {'groups': groups}
        )


class PositionCreate(generic.CreateView):
    """Create a position"""
    model = Position
    fields = PositionForm.Meta.fields + ['representative']

    def get_success_url(self):
        return PositionsRepresentative(slug=self.object.representative.slug).get_absolute_url()


class PositionDetail(generic.DetailView):
    """Display a position"""
    model = Position
    queryset = Position.objects.filter(published=True)
