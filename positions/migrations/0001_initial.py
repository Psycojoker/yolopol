# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0010_index_group_kind_and_abbreviation'),
        ('representatives_votes', '0008_unique_proposal_title'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateField()),
                ('text', models.TextField()),
                ('link', models.URLField()),
                ('published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recommendation', models.CharField(max_length=10, choices=[(b'abstain', b'abstain'), (b'for', b'for'), (b'against', b'against')])),
                ('title', models.CharField(max_length=1000, blank=True)),
                ('description', models.TextField(blank=True)),
                ('weight', models.IntegerField(default=0)),
                ('proposal', models.OneToOneField(related_name='recommendation', to='representatives_votes.Proposal')),
            ],
            options={
                'ordering': ['proposal__datetime'],
            },
        ),
        migrations.CreateModel(
            name='RepresentativeVoteProfile',
            fields=[
                ('representative', models.OneToOneField(related_name='votes_profile', primary_key=True, serialize=False, to='representatives.Representative')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PositionsRepresentative',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('representatives.representative',),
        ),
        migrations.CreateModel(
            name='PositionsVote',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('representatives_votes.vote',),
        ),
        migrations.AddField(
            model_name='position',
            name='representative',
            field=models.ForeignKey(related_name='positions', to='representatives.Representative'),
        ),
        migrations.AddField(
            model_name='position',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
