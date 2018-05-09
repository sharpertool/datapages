from django.db import models


from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Page, Orderable

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from datasheet.models import SheetBasePage, IndexBasePage
from datasheet.blocks import (DimensionBlock, ChartBlock, CharacteristicsBlock, VideoBlock, Embed3DBlock, GridDataBlock,
                              PDFBlock)
from .blocks import (ContactDataBlock, CoilDataBlock, RelayProductCodeStructureBlock, RevisionBlock, FeaturesBlock,
                     ApplicationsBlock, CarouselImageBlock, CarouselEmbedBlock, CarouselFusionEmbedBlock)


class SheetPageTag(TaggedItemBase):
    content_object = ParentalKey('SheetPage', related_name='tagged_items')


class IndexPage(IndexBasePage):
    """
    The index or home page for TE Connectivity.
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='teconn_index')

    class Meta:
        verbose_name = "TE Connectivity Index Page"


class SheetPage(SheetBasePage):
    """
    The product page and details. Common fields are already declared in SheetBasePage abstract class
    so you just have to declare here the sheet_blocks field base on TE connectivity requirements.
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='teconn_sheet')

    sheet_blocks = StreamField([
        ('contact_data', ContactDataBlock()),
        ('coil_data', CoilDataBlock()),
        ('dimension', DimensionBlock()),
        ('product_code', RelayProductCodeStructureBlock()),
        ('revisions', RevisionBlock()),
        ('characteristics', CharacteristicsBlock()),
        ('chart', ChartBlock()),
        ('video', VideoBlock()),
        ('embed_3d', Embed3DBlock()),
        ('grid', GridDataBlock()),
        ('pdf', PDFBlock())
    ], blank=True)
    attributes = StreamField([
        ('features', FeaturesBlock()),
        ('applications', ApplicationsBlock())
    ], blank=True)
    carousel = StreamField([
        ('image', CarouselImageBlock()),
        ('embed', CarouselEmbedBlock()),
        ('fusion360', CarouselFusionEmbedBlock()),
    ], blank=True)

    parent_page_types = ['IndexPage']

    tags = ClusterTaggableManager(through=SheetPageTag, blank=True, related_name='teconn_sheetpage_tags')

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


class RelatedLinks(Orderable):
    page = ParentalKey(SheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
