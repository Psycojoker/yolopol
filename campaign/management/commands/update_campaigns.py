from django.core.management.base import BaseCommand

from representatives_votes.models import Dossier

from ...models import Campaign


class Command(BaseCommand):
    def handle(self, *args, **options):
        dossiers = Dossier.objects.filter(
            pk__in=Campaign.objects.values_list('dossiers')
        )

        for dossier in dossiers:
            dossier.sync()
