from django.core.management import BaseCommand
from ...models import Ranking

class Command(BaseCommand):

    def handle(self, *args, **options):
        Ranking.objects.all().delete()