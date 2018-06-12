from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, InlinePanel, FieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.core import blocks

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from datasheet.models import IndexBasePage, SheetBasePage
from datasheet.blocks import (SelectorBlock, DimensionBlock, GridDataBlock, ChartBlock,
                              CharacteristicsBlock, VideoBlock,
                              Embed3DBlock, PDFBlock, RichTextBlock)
from teconn.blocks import (CarouselEmbedBlock, CarouselFusionEmbedBlock,
                           FeaturesBlock, ApplicationsBlock,
                           ContactDataBlock, RelayProductCodeStructureBlock)
from .blocks import PanasonicCarouselImageBlock, PartSelectorBlock


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
        ('specification', ContactDataBlock()),
        ('grid', GridDataBlock()),
        ('selector', SelectorBlock()),
        ('dimension', DimensionBlock()),
        ('product_code', RelayProductCodeStructureBlock()),
        ('chart', ChartBlock()),
        ('characteristics', CharacteristicsBlock()),
        ('video', VideoBlock()),
        ('embed_3d', Embed3DBlock()),
        ('pdf', PDFBlock()),
        ('richtext', blocks.RichTextBlock()),
        ('part_selector', PartSelectorBlock()),
        ('richtext', RichTextBlock()),
    ], blank=True)

    attributes = StreamField([
        ('features', FeaturesBlock()),
        ('applications', ApplicationsBlock())
    ], blank=True)

    carousel = StreamField([
        ('image', PanasonicCarouselImageBlock()),
        ('embed', CarouselEmbedBlock()),
        ('fusion360', CarouselFusionEmbedBlock()),
    ], blank=True)

    parent_page_types = ['panasonic.IndexPage']

    tags = ClusterTaggableManager(through=SheetPageTag, blank=True, related_name='sheetpage_tags')

    content_panels = SheetBasePage.content_panels + [
        MultiFieldPanel([
            StreamFieldPanel('attributes', heading=None, classname="full"),
        ],
            heading="Attributes and Applications",
            classname="collapsible collapsed"),
        StreamFieldPanel('carousel'),
        StreamFieldPanel('sheet_blocks', heading="Blocks"),
        InlinePanel('related_links', label="Related Links")
    ]

    def get_context(self, request):
        """ calculate the max number of attributes, for styling. """
        context = super().get_context(request)
        return context


class RelatedLinks(Orderable):
    page = ParentalKey(SheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
