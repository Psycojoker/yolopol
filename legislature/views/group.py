# coding: utf-8

from datetime import datetime

from django.shortcuts import render

from representatives.models import Group


def index(request, kind=None):
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
