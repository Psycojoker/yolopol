# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0008_unique_proposal_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('dossiers', models.ManyToManyField(to='representatives_votes.Dossier')),
            ],
        ),
    ]
