from django.db import models

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel
from wagtail.core.models import Orderable

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from datasheet.models import SheetBasePage, IndexBasePage
from datasheet.blocks import DimensionBlock
from .blocks import ContactDataBlock, CoilDataBlock, RelayProductCodeStructureBlock, RevisionBlock


class SheetPageTag(TaggedItemBase):
    content_object = ParentalKey('SheetPage', related_name='tagged_items')


class IndexPage(IndexBasePage):
    """
    The index or home page for TE Connectivity.
    """
    class Meta:
        verbose_name = "TE Connectivity Index Page"


class SheetPage(SheetBasePage):
    """
    The product page and details. Common fields are already declared in SheetBasePage abstract class
    so you just have to declare here the sheet_blocks field base on TE connectivity requirements.
    """
    sheet_blocks = StreamField([
        ('contact_data', ContactDataBlock()),
        ('coild_data', CoilDataBlock()),
        ('dimension', DimensionBlock()),
        ('product_code', RelayProductCodeStructureBlock()),
        ('revisions', RevisionBlock())
    ], blank=True)

    tags = ClusterTaggableManager(through=SheetPageTag, blank=True)

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
