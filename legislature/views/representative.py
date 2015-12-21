# coding: utf-8

from __future__ import absolute_import

from datetime import datetime

from django.db.models import Q, Prefetch
from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify

from core.utils import render_paginate_list
from positions.forms import PositionForm

from representatives.models import Representative


def index(request, group_kind=None, group=None):

    # Fetch active representatives
    representative_list = Representative.objects.filter(active=True)

    # Filter the list by group if group information is provided
    if group_kind:
        if group.isnumeric():
            representative_list = representative_list.filter(
                mandates__group_id=int(group),
                mandates__end_date__gte=datetime.now()
            )
        else:
            # Search group based on abbreviation or name
            representative_list = representative_list.filter(
                Q(mandates__group__abbreviation=group) |
                Q(mandates__group__name=group),
                mandates__group__kind=group_kind,
                mandates__end_date__gte=datetime.now()
            )

    # Filter the list by search
    representative_list = _filter_by_search(
        request,
        representative_list
    ).order_by('-votes_profile__score', 'last_name')

    # Grid or list
    if request.GET.get('display') in ('grid', 'list'):
        request.session['display'] = request.GET.get('display')
    if 'display' not in request.session:
        request.session['display'] = 'grid'

    representative_list = representative_list.select_related('votes_profile')
    representative_list = Representative.objects.prefetch_profile(
        representative_list)

    # Render the paginated template
    return render_paginate_list(
        request,
        representative_list,
        'legislature/representative_{}.html'.format(
            request.session['display']
        )
    )


def detail(request, name=None):
    query_set = Representative.objects.select_related(
        'country',
        'main_mandate'
    )

    try:
        representative = query_set.get(slug=name)
    except Representative.DoesNotExist:
        return Http404()

    position_form = PositionForm()
    return render(
        request,
        'legislature/representative_detail.html',
        {
            'representative': representative,
            'position_form': position_form
        }
    )


def _filter_by_search(request, representative_list):
    """
    Return a representative_list filtered by
    the representative name provided in search form
    """
    search = request.GET.get('search')
    if search:
        return representative_list.filter(
            Q(slug__icontains=slugify(search))
        )
    else:
        return representative_list
