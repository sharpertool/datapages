import fitz
import os
import re
import sys
import time

from microchip.models import SheetPage, SheetSubPage


def load_toc_from_pdf(pdf_file):
    """ Use mupudf to load the table of contents """
    doc = fitz.open(pdf_file)
    toc = doc.getToC()
    return toc


def create_page(section, title, page):
    p = SheetSubPage(section_number=section,
                     title=title,
                     pdf_page=page)
    return p


def get_section_number(title):
    m = re.search(r'^([0-9\.]+)\s', title)
    if m:
        return m.group(1)
    return None


def build_flat_hierarchy_from_toc(slug='', toc=None, clear=False):
    """
    Build a flat hierarchy on the page identified by the slug

    clear=True will remove all existing sub-pages first

    Each TOC item is an array of [depth, title, page]
    :param slug:
    :param toc:
    :return:
    """

    parent = SheetPage.objects.get(slug=slug)

    if clear:
        for d in parent.get_descendants():
            d.delete()

    depth_previous = toc[0][0]
    curr_parent = parent
    parents_by_depth = {}
    for depth, title, page in toc:

        section_number = get_section_number(title)

        if depth < depth_previous:
            if depth == 1:
                curr_parent = parent
            else:
                curr_parent = parents_by_depth[depth - 1]

            newpage = create_page(section_number, title, page)
            page = curr_parent.add_child(instance=newpage)
            parents_by_depth[depth] = page

        elif depth == depth_previous:
            newpage = create_page(section_number, title, page)
            page = curr_parent.add_child(instance=newpage)
            parents_by_depth[depth] = page

        elif depth > depth_previous:
            curr_parent = parents_by_depth[depth_previous]

            newpage = create_page(section_number, title, page)
            page = curr_parent.add_child(instance=newpage)
            parents_by_depth[depth] = page

        depth_previous = depth
