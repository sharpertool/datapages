from os.path import exists, expanduser
import re
from shutil import copy
import sys
from textwrap import dedent

from django.core.management.base import BaseCommand
from datapages.utils.pdfutils import build_flat_hierarchy_from_toc, load_toc_from_pdf


class Command(BaseCommand):
    help = 'Import a datasheet table of contents into the specified datasheet'

    def add_arguments(self, parser):
        parser.add_argument('parent_slug',
                            help=dedent("""
                Specify the slug of the parent datasheet.
                    """))

        parser.add_argument('pdf_file',
                            help=dedent("""
                            Specify the pdf file to extract the toc from.
                            """))

    def handle(self, *args, **options):
        slug = options.get('parent_slug')
        pdffile = expanduser(options.get('pdf_file'))

        if not exists(pdffile):
            raise Exception(f"The pdffile \"{pdffile}\" does not exist.")

        print(f"Loading table of contents from \"{pdffile}\" into page:{slug} ")
        toc = load_toc_from_pdf(pdffile)
        build_flat_hierarchy_from_toc(slug=slug, toc=toc, clear=True)

