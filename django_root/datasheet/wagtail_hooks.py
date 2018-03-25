from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib.staticfiles.templatetags.staticfiles import static

from wagtail.admin.site_summary import SummaryItem
from wagtail.core import hooks

from .models import DatasheetPage


class DatasheetPanel:
    order = 50

    def render(self):
        return mark_safe("""
        <section class="anel summary nice-padding">
            <h2>Welcome to the DataPages Interface</h2>
            <h3>We Welcome our TE users!</h3>
        </section>
        """)


@hooks.register('construct_homepage_panels')
def add_datapages_panel(request, panels):
    return panels.append(DatasheetPanel())


class DatasheetSummary(SummaryItem):
    template = "datasheet/summary/datasheet_summary_pages.html"

    def get_context(self):
        """
        Return count of the number of datasheets
        :return:
        """
        DatasheetPage.objects.count()
        return {
            'total_pages': DatasheetPage.objects.count()
        }


@hooks.register('construct_homepage_summary_items')
def add_datasheet_summary(request, items):

    return items.append(DatasheetSummary(request))


@hooks.register('product_code')
def product_code_hook():
    pass

@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}"',
        static('css/datasheetadmin.css')
    )