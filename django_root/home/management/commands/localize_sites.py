import re
from django.core.management.base import BaseCommand
from wagtail.core.models import Site


class Command(BaseCommand):
    help = 'Convert sites to *.local and update their port'

    def add_arguments(self, parser):
        parser.add_argument('--port', type=int, default=8000)

    def handle(self, *args, **options):
        newport = options.get('port')
        sites = Site.objects.all()
        for site in sites:
            newhost = re.sub(r'\.io$', '.local', site.hostname)
            if newhost != site.hostname or site.port != newport:
                print(f"Updating {site.hostname} to {newhost} and Port from {site.port} to {newport}")
                site.hostname = newhost
                site.port = newport
                site.save()



