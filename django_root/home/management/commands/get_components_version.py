import re
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Print the value of the components version'

    def add_arguments(self, parser):
        parser.add_argument('tmpfile', help='''
        Temporary file to write the version to
        ''')

    def handle(self, *args, **options):

        with open(options.get('tmpfile'), 'w') as fp:
            fp.write(f"{settings.COMPONENTS_VERSION}")



