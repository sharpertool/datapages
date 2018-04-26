from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, InlinePanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from datasheet.models import IndexBasePage, SheetBasePage
from datasheet.blocks import SelectorBlock, DimensionBlock, GridDataBlock, ChartBlock


class SheetPageTag(TaggedItemBase):
    content_object = ParentalKey('SheetPage', related_name='tagged_items')


# Create your models here.
class IndexPage(IndexBasePage):
    """
    The index or home page for panasonic
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='panasonic_index')

    subpage_types = ['panasonic.SheetPage']

    class Meta:
        verbose_name = "Panasonic Index Page"


class SheetPage(SheetBasePage):
    """
    Subpage for panasonic indexpage
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='panasonic_sheet')

    sheet_blocks = StreamField([
        ('grid', GridDataBlock()),
        ('selector', SelectorBlock()),
        ('dimension', DimensionBlock()),
        ('chart', ChartBlock())
    ])

    parent_page_types = ['panasonic.IndexPage']

    tags = ClusterTaggableManager(through=SheetPageTag, blank=True, related_name='sheetpage_tags')

    content_panels = SheetBasePage.content_panels + [
        StreamFieldPanel('sheet_blocks', heading="Blocks"),
        InlinePanel('related_links', label="Related Links")
    ]


class RelatedLinks(Orderable):
    page = ParentalKey(SheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
