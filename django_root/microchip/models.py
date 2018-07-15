from django.db import models


from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (StreamFieldPanel, FieldPanel,
                                         InlinePanel, MultiFieldPanel)
from wagtail.core.models import Page, Orderable

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from datasheet.models import IndexBasePage, SheetBasePage
from datasheet.blocks import (DimensionBlock, ChartBlock,
                              CharacteristicsBlock, VideoBlock,
                              Embed3DBlock, GridDataBlock,
                              PDFBlock, RichTextBlock)
from onsemi.blocks import FeaturesBlock, ApplicationsBlock, CarouselImageBlock


class SheetPageTag(TaggedItemBase):
    content_object = ParentalKey('SheetPage', related_name='tagged_items')


class IndexPage(IndexBasePage):
    """
    The index or home page.
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='microchip_index')

    class Meta:
        verbose_name = "Microchip Index Page"


class SheetPage(SheetBasePage):
    """
    The product page and details. Common fields are already declared in SheetBasePage abstract class
    so you just have to declare here the sheet_blocks field base on site requirements.
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='microchip_sheet')

    sheet_blocks = StreamField([
        ('dimension', DimensionBlock()),
        ('characteristics', CharacteristicsBlock()),
        ('chart', ChartBlock()),
        ('video', VideoBlock()),
        ('embed_3d', Embed3DBlock()),
        ('grid', GridDataBlock()),
        ('pdf', PDFBlock()),
        ('richtext', RichTextBlock()),
    ], blank=True)

    attributes = StreamField([
        ('features', FeaturesBlock()),
        ('applications', ApplicationsBlock())
    ], blank=True)

    carousel = StreamField([
        ('image', CarouselImageBlock()),
    ], blank=True)

    parent_page_types = ['IndexPage']

    tags = ClusterTaggableManager(through=SheetPageTag,
                                  blank=True, related_name='microchip_sheetpage_tags')

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

    subpage_types = ['microchip.SheetSubPage']

    def my_children(self):
        """ Return children, in section sort order. """
        children = [obj.specific for obj in self.get_children()]
        return children


class SheetSubPage(Page):

    section_number = models.CharField(max_length=128, null=True, blank=True)
    pdf_page = models.IntegerField(null=True, blank=True)

    stream = StreamField([
        ('dimension', DimensionBlock()),
        ('characteristics', CharacteristicsBlock()),
        ('chart', ChartBlock()),
        ('video', VideoBlock()),
        ('embed_3d', Embed3DBlock()),
        ('grid', GridDataBlock()),
        ('pdf', PDFBlock()),
        ('richtext', RichTextBlock()),
    ], blank=True)

    parent_page_types = ['microchip.SheetPage', 'microchip.SheetSubPage']
    subpage_types = ['microchip.SheetSubPage']

    content_panels = Page.content_panels + [
        FieldPanel('section_number'),
        FieldPanel('pdf_page'),
        StreamFieldPanel('stream', heading="Blocks"),
    ]


class RelatedLinks(Orderable):
    page = ParentalKey(SheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
