from django.contrib import admin
from django.db import connection, models
from django.http import HttpResponseRedirect

from representatives.models import Representative
from representatives_votes.models import Dossier, Vote
from representatives_positions.models import Position


class VoteScore(models.Model):
    vote = models.OneToOneField(Vote, related_name='vote_score')
    score = models.FloatField()

    @classmethod
    def refresh(cls):
        with connection.cursor() as cursor:
            cursor.execute('SELECT refresh_vote_scores();')


class DossierScore(models.Model):
    representative = models.ForeignKey(Representative,
                                       related_name='dossier_scores')
    dossier = models.ForeignKey(Dossier)
    score = models.FloatField()

    @classmethod
    def refresh(cls):
        with connection.cursor() as cursor:
            cursor.execute('SELECT refresh_dossier_scores();')


class PositionScore(models.Model):
    position = models.OneToOneField(Position, related_name='position_score')
    score = models.FloatField()

    @classmethod
    def refresh(cls):
        with connection.cursor() as cursor:
            cursor.execute('SELECT refresh_position_scores();')


class RepresentativeScore(models.Model):
    representative = models.OneToOneField(Representative,
                                          related_name='representative_score')
    score = models.FloatField()

    @classmethod
    def refresh(cls):
        with connection.cursor() as cursor:
            cursor.execute('SELECT refresh_representative_scores();')


def refresh_scores(modeladmin, request, queryset):
    RepresentativeScore.refresh()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


refresh_scores.short_description = 'Refresh representative scores'
admin.site.add_action(refresh_scores, 'refresh_scores')
