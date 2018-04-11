#!/bin/env python


import argparse
import os
import os.path
from pathlib import Path
import re

class Filter:
    search_pat=""
    replace_pat=""

    def __init__(self):
        self.spat = re.compile(self.search_pat)

    def to_nunjucks(self, line):
        m = self.spat.search(line)
        if m:
            return self.spat.sub(self.replace_pat, line)
        return line

    def to_django(self, line):
        """ Reverse the operation """
        return line

    def indent(self, line):
        """ return the space indentation """
        m = re.search(r'^(\s*)', line)
        if m:
            return m.group(1)
        return ''


class LoadFilter(Filter):
    search_pat = r"\{\%(\s*load\s+.*)\%\}"
    replace_pat = r"<!-- DJANGO_LOAD \1 -->"


class IncludeFilter(Filter):
    search_pat = r"\{\%(\s*include_block\s+.*)\%\}"
    replace_pat = r"<!-- DJANGO_INCLUDE_BLOCK \1 -->"


class ImageFilter(Filter):
    search_pat = r"\{\%(\s*image\s+.*)\%\}"
    replace_pat = r"<!-- DJANGO_IMAGE \1 -->"

class WagtailFilter(Filter):
    search_pat = r"\{\%\s*wagtailuserbar\s*\%\}"
    replace_pat = r"<!-- WAGTAIL_USER_BAR -->"

class HrefFilter(Filter):
    search_pat = r"href=\"\{\%\s*static\s+[\"'](.*?)[\"']\s*\%\}\""

    def to_nunjucks(self, line):
        m = self.spat.search(line)
        if m:
            url = m.group(1)
            purl = os.path.splitext(url)[0] + '.processed.css'
            rpat = f'href="{purl}"'
            i = self.indent(line)
            line = f"\n{i}<!-- OLDHREF {url} -->\n" + self.spat.sub(rpat, line)
            return line
        return line

class StaticSrcFilter(Filter):
    search_pat = r"src=\"\{\%\s*static\s+[\"'](.*?)[\"']\s*\%\}\""

    def to_nunjucks(self, line):
        m = self.spat.search(line)
        if m:
            url = m.group(1)
            purl = url
            rpat = f'src="{purl}"'
            i = self.indent(line)
            line = f"\n{i}<!-- OLDSTATIC {url} -->\n" + self.spat.sub(rpat, line)
            return line
        return line

class WithFilter(Filter):
    search_pat = r"\{\%\s*with\s*(.*)\%\}"
    replace_pat = r"<!-- DJANGO_WITH \1 --> \n<!--"

class EndWithFilter(Filter):
    search_pat = r"\{\%\s*endwith(.*)\%\}"
    replace_pat = r"-->\n <!-- DJANGO_ENDWITH \1 -->"

class IncludeFileFilter(Filter):
    search_pat = r'\{\%\s*(include|extends)\s*["\'](.*.html)["\'].*\%\}'

    def to_nunjucks(self, line):
        m = self.spat.search(line)
        if m:
            line = re.sub('\.html', '.njk', line)

        return line

class ToNunjucks:

    def __init__(self):

        self.filters = [
            LoadFilter(),
            IncludeFilter(),
            ImageFilter(),
            HrefFilter(),
            WithFilter(),
            EndWithFilter(),
            IncludeFileFilter(),
            StaticSrcFilter(),
            WagtailFilter(),
        ]

    def filter_line(self, line):
        """ Apply all filters to the line """
        for f in self.filters:
            line = f.to_nunjucks(line)

        return line

    def filter(self, src, dest):
        """
        Open the sourc, and write to dest, with some filter operations
        :param src:
        :param dest:
        :return:
        """

        Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)

        with open(src, 'r') as fp:
            with open(dest, 'w') as fp2:
                for line in fp:
                    line = self.filter_line(line)

                    fp2.write(line)

    def filter_load(self, line):
        pass

    def filter_include(self, line):
        pass

    def filter_image(self, line):
        pass

    def filter_href(self, line):
        pass

def to_nunjucks(src, dest):
    """
    Open the sourc, and write to dest, with some filter operations
    :param src:
    :param dest:
    :return:
    """

    p = ToNunjucks()
    p.filter(src, dest)


def to_django(src, dest):
    """
    Open the sourc, and write to dest, with some filter operations
    :param src:
    :param dest:
    :return:
    """

    Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)

    with open(src, 'r') as fp:
        with open(dest, 'w') as fp2:
            for line in fp:
                line = re.sub(r"<!-- DJANGO_REQUIRED (.*) -->", r"\1", line)
                fp2.write(line)


def django_to_nunjucks(top, dest):
    print(f"Descending into {top}")
    # Delete everything reachable from the directory named in "top",
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    for root, dirs, files in os.walk(top, topdown=False):
        rel_root = os.path.relpath(root, top)

        for name in [f for f in files if f.endswith('.html')]:
            njname = os.path.splitext(name)[0] + '.njk'
            src_file = os.path.join(root, name)
            dest_file = os.path.join(dest, rel_root, njname)
            print(f"Stream {src_file}  {dest_file}")
            to_nunjucks(src_file, dest_file)


def nunjucks_to_django(njkdir, djdir):
    print(f"Descending into {top}")
    # Delete everything reachable from the directory named in "top",
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    for root, dirs, files in os.walk(njkdir, topdown=False):
        rel_root = os.path.relpath(root, njkdir)

        for name in [f for f in files if f.endswith('.njk')]:
            njname = os.path.splitext(name)[0] + '.html'
            src_file = os.path.join(root, name)
            dest_file = os.path.join(djdir, rel_root, njname)
            print(f"Stream {src_file}  {dest_file}")
            to_django(src_file, dest_file)


def main():
    """
    Main driver for the script.

    """

    parser = argparse.ArgumentParser(description="Copy templates to njk format")

    parser.add_argument("root",
                        help="Root Path to start from.")

    parser.add_argument("dest",
                        help="Destination folder")

    parser.add_argument("--main_file",
                        default="django_root/datasheet/templates/datasheet/datasheet_page.html")

    parser.add_argument("--context_file",
                        default="datasheet_codepen_context.njk")


    args = parser.parse_args()

    django_to_nunjucks(args.root, args.dest)
    django_to_nunjucks("django_root/templates", args.dest)


if __name__ == "__main__":
    main()
