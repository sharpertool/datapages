from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, InlinePanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from datasheet.models import IndexBasePage, SheetBasePage
from datasheet.blocks import SelectorBlock, DimensionBlock


class SheetPageTag(TaggedItemBase):
    content_object = ParentalKey('PanasonicSheetPage', related_name='tagged_items')


# Create your models here.
class PanasonicIndexPage(IndexBasePage):
    """
    The index or home page for panasonic
    """

    subpage_types = ['PanasonicSheetPage']

    class Meta:
        verbose_name = "Panasonic Index Page"


class PanasonicSheetPage(SheetBasePage):
    """
    Subpage for panasonic indexpage
    """
    sheet_blocks = StreamField([
        ('selector', SelectorBlock()),
        ('dimension', DimensionBlock())
    ])

    parent_page_types = ['PanasonicIndexPage']

    tags = ClusterTaggableManager(through=SheetPageTag, blank=True, related_name='panasonic_sheetpage_tags')

    content_panels = SheetBasePage.content_panels + [
        StreamFieldPanel('sheet_blocks', heading="Blocks"),
        InlinePanel('related_links', label="Related Links")
    ]


class RelatedLinks(Orderable):
    page = ParentalKey(PanasonicSheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
