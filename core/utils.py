from __future__ import absolute_import

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import render


def create_child_instance_from_parent(child_cls, parent_instance):
    """
    Create a child model instance from a parent instance
    """
    parent_cls = parent_instance.__class__
    field = child_cls._meta.get_ancestor_link(parent_cls).column

    child_instance = child_cls(**{
        field: parent_instance.pk
    })

    child_instance.__dict__.update(parent_instance.__dict__)
    child_instance.save()
    return child_instance


def render_paginate_list(request, object_list, template_name):
    """
    Render a paginated list of representatives
    """
    pagination_limits = (10, 20, 50, 100)
    num_by_page = request.GET.get('limit', 30)
    paginator = Paginator(object_list, num_by_page)
    page = request.GET.get('page', 1)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {}
    queries_without_page = request.GET.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']
    context['queries'] = queries_without_page
    context['object_list'] = objects
    context['paginator'] = paginator
    context['pagination_limits'] = pagination_limits

    return render(
        request,
        template_name,
        context
    )
