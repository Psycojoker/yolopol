# coding: utf-8
from __future__ import absolute_import

from django.contrib import admin

from autocomplete_light import shortcuts as ac

from .models import Recommendation


class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'proposal', 'recommendation', 'weight')
    search_fields = ('title', 'recommendation', 'proposal')
    form = ac.modelform_factory(Recommendation, exclude=[])

admin.site.register(Recommendation, RecommendationsAdmin)
