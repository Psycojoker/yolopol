# coding: utf-8
from __future__ import absolute_import

from django.contrib import admin

from .models import Position
from autocomplete_light import shortcuts as ac

from .models import Recommendation


def publish_positions(modeladmin, request, queryset):
    """Set published to True for the queryset"""
    queryset.update(published=True)

publish_positions.short_description = 'Publish selected positions'


def unpublish_positions(modeladmin, request, queryset):
    """Set published to False for the queryset"""
    queryset.update(published=False)

unpublish_positions.short_description = 'Unpublish selected positions'


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'representative',
        'short_text',
        'datetime',
        'link',
        'published')
    list_display_links = ('short_text',)
    list_editable = ('published',)
    list_filter = ('published',)
    actions = (publish_positions, unpublish_positions)

admin.site.register(Position, PositionAdmin)


class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'proposal', 'recommendation', 'weight')
    search_fields = ('title', 'recommendation', 'proposal')
    form = ac.modelform_factory(Recommendation, exclude=[])

admin.site.register(Recommendation, RecommendationsAdmin)
