import os

from autoslug import AutoSlugField

from django.db import models



class Campaign(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')
    dossiers = models.ManyToManyField('representatives_votes.dossier')

    def __unicode__(self):
        return self.name
