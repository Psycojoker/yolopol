# coding: utf-8
"""
Positions model.

This app adds Recommendation and Position models to
representatives.Representative, and also couples representatives_votes.Vote for
RepresentativeVoteProfile which contains a score.
"""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager
from representatives_votes.contrib.parltrack.import_votes import \
    vote_pre_import
from representatives_votes.models import Dossier, Proposal, Vote
from representatives.models import Representative


class PositionsRepresentative(Representative):
    def get_absolute_url(self):
        return reverse('positions:representative-detail', args=(self.slug,))

    class Meta:
        proxy = True


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


class PositionsVote(Vote):
    class Meta:
        proxy = True

    @cached_property
    def absolute_score(self):
        recommendation = self.proposal.recommendation

        if self.position == recommendation.recommendation:
            return recommendation.weight
        else:
            return -recommendation.weight



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
    votes = representative.votes.exclude(proposal__recommendation=None
            ).select_related('proposal__recommendation')
    votes = PositionsVote.objects.filter(pk__in=votes.values_list('pk'))

    for vote in votes:
        score += vote.absolute_score

    return score


class Position(models.Model):
    representative = models.ForeignKey(Representative,
            related_name='positions')
    datetime = models.DateField()
    text = models.TextField()
    link = models.URLField()
    published = models.BooleanField(default=False)
    tags = TaggableManager()

    @property
    def short_text(self):
        return truncatewords(self.text, 5)

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False

    def get_absolute_url(self):
        return reverse('positions:position-detail', args=(self.pk,))
