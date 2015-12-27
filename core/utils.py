from __future__ import absolute_import

from pure_pagination import EmptyPage
from pure_pagination import Paginator
from django.shortcuts import render


def render_paginate_list(request, object_list, template_name):
    """
    Render a paginated list of representatives
    """
    pagination_limits = (12, 24, 48, 96)
    num_by_page = request.GET.get('limit', unicode(pagination_limits[0]))
    num_by_page = int(num_by_page) if num_by_page.isdigit() else 1
    paginator = Paginator(object_list, num_by_page)
    number = request.GET.get('page', '1')
    number = int(number) if number.isdigit() else 1

    try:
        page = paginator.page(number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {}
    context['paginator'] = paginator
    context['page'] = page
    context['object_list'] = context['page'].object_list
    context['pagination_limits'] = pagination_limits

    return render(
        request,
        template_name,
        context
    )
