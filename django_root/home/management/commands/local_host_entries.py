from os.path import exists
import re
from shutil import copy
from textwrap import dedent

from django.core.management.base import BaseCommand
from wagtail.core.models import Site


class Command(BaseCommand):
    help = 'Generate output to be added to /etc/hosts file'

    def add_arguments(self, parser):
        parser.add_argument('--env')
        parser.add_argument('--etcfile')

    def handle(self, *args, **options):

        allowed_hosts = list(
            Site.objects.values_list('hostname', flat=True).all())

        etc_hosts = [f"127.0.0.1 {x}" for x in allowed_hosts]

        hosts_lines = "\n".join(etc_hosts)

        etc_data = "# Datapages.local begin\n" + hosts_lines + "\n# Datapages.local end\n"

        envfile = options.get('env', None)
        if envfile and exists(envfile):
            copy(envfile, envfile + '.bak')
            with open(envfile, 'r') as fp:
                original = fp.readlines()

            with open(envfile, 'w') as fp:
                for line in original:
                    if re.search(r'^DJANGO_ALLOWED_HOSTS', line):
                        line = f"DJANGO_ALLOWED_HOSTS={','.join(allowed_hosts)}"
                    fp.write(line)

        hostsfile = options.get('etcfile', None)
        if hostsfile:
            print(etc_data)
