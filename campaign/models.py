import os

from autoslug import AutoSlugField

from django.db import models

import django_rq

from representatives_votes.models import Dossier
from representatives_votes.signals import sync


class Campaign(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')
    dossiers = models.ManyToManyField('representatives_votes.dossier')

    def __unicode__(self):
        return self.name


def dossier_sync_job(pk):
    sync.send(sender=Dossier, instance=Dossier.objects.get(pk=pk))


def campaign_dossiers_sync(sender, instance, **kwargs):
    queue = django_rq.get_queue('default')

    for dossier in instance.dossiers.all():
        queue.enqueue(dossier_sync_job, dossier.pk)
models.signals.post_save.connect(campaign_dossiers_sync, sender=Campaign)
