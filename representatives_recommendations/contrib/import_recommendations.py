# coding: utf-8

import csv
import django
from django.apps import apps
import logging
import sys

from representatives_recommendations.models import Recommendation
from representatives_votes.models import Dossier, Proposal

from .import_data import dossier_mappings, resolutions

logger = logging.getLogger(__name__)


class RecommendationImporter:
    def __init__(self):
        self.dossier_cache = {}

    def get_dossier(self, title):
        dossier = self.dossier_cache.get(title, None)

        if dossier is None:
            ref = dossier_mappings.get(title, None)
            if ref is not None:
                query = {'reference': ref}
            else:
                query = {'title__iexact': title}

            try:
                dossier = Dossier.objects.get(**query)
                self.dossier_cache[title] = dossier
            except Dossier.DoesNotExist:
                dossier = None

        return dossier

    def get_proposal(self, dossier, kind):
        kinds = [kind]

        try:
            resolutions.index(kind.lower())
            kinds.extend(resolutions)
        except ValueError:
            pass

        for k in kinds:
            try:
                return Proposal.objects.get(dossier=dossier, kind__iexact=k)
            except Proposal.DoesNotExist:
                continue

        return None

    def import_row(self, row):
        dossier = self.get_dossier(row['title'])
        if dossier is None:
            logger.warn('No dossier "%s"' % row['title'])
            return False

        proposal = self.get_proposal(dossier, row['part'])
        if proposal is None:
            logger.warn('No proposal "%s" for dossier %s (%d): "%s"' % (
                row['part'].decode('utf-8'), dossier.reference, dossier.pk,
                row['title']))
            return False

        weight = int(row['weight']) * int(row['ponderation'])
        descr = row['description'].strip()
        if len(descr) == 0:
            descr = '%s on %s' % (row['part'], dossier.reference)

        try:
            recom = Recommendation.objects.get(proposal=proposal)
        except Recommendation.DoesNotExist:
            recom = Recommendation(
                proposal=proposal,
                recommendation=row['recommendation'],
                title=descr,
                weight=weight
            )
            recom.save()
            logger.info('Created recommendation with weight %s for %s: %s' % (
                weight,
                row['title'],
                row['part']
            ))

        return True


def main(stream=None):
    """
    Imports recommendations from an old memopol instance.

    Usage:
        cat recommendations.csv | memopol_import_recommendations

    The input CSV file should be generated by the following query:
        SELECT CONCAT(r.description, '|', r.weight, '|', r.recommendation, '|',
            r.part, '|', p.title, '|', p.ponderation)
        FROM votes_recommendation r
            LEFT JOIN votes_proposal p ON r.proposal_id = p.id
        WHERE p.institution = 'EU'

    """

    if not apps.ready:
        django.setup()

    importer = RecommendationImporter()
    rejected = []
    imported = 0

    reader = csv.DictReader(stream or sys.stdin, delimiter='|', fieldnames=[
        'description',
        'weight',
        'recommendation',
        'part',
        'title',
        'ponderation'
    ], quoting=csv.QUOTE_NONE)

    for row in reader:
        if not importer.import_row(row):
            rejected.append(row)
        else:
            imported = imported + 1

    logger.info('%d rows imported, %d rows rejected', imported, len(rejected))
