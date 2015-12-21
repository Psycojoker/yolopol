# coding: utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from representatives_votes.contrib.parltrack.import_votes import \
    vote_pre_import
from representatives_votes.models import Dossier, Proposal, Vote
from representatives.models import Representative


class RepresentativeVoteProfile(models.Model):
    representative = models.OneToOneField('representatives.representative',
        primary_key=True, related_name='votes_profile')
    score = models.IntegerField(default=0)


class Recommendation(models.Model):
    proposal = models.OneToOneField(
        Proposal,
        related_name='recommendation'
    )

    recommendation = models.CharField(max_length=10, choices=Vote.VOTECHOICES)
    title = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        ordering = ['proposal__datetime']


def skip_votes(sender, vote_data=None, **kwargs):
    dossiers = getattr(sender, 'memopol_filters', None)

    if dossiers is None:
        sender.memopol_filters = dossiers = Dossier.objects.filter(
            proposals__recommendation__in=Recommendation.objects.all()
        ).values_list('reference', flat=True)

    if vote_data.get('epref', None) not in dossiers:
        return False
vote_pre_import.connect(skip_votes)


def create_representative_vote_profile(sender, instance=None, created=None,
        **kwargs):

    if not created:
        return

    RepresentativeVoteProfile.objects.create(representative=instance)
post_save.connect(create_representative_vote_profile, sender=Representative)


def calculate_representative_score(representative):
    score = 0

    for vote in representative.votes.all():
        try:
            recommendation = Recommendation.objects.get(
                proposal_id=vote.proposal_id)
        except Recommendation.DoesNotExist:
            # Catch an exception to avoid un-necessary queries
            continue

        if recommendation.recommendation == vote.position:
            score += recommendation.weight
        else:
            score -= recommendation.weight

    return score
