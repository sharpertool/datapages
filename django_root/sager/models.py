from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, InlinePanel, FieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable

from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from datasheet.models import IndexBasePage, SheetBasePage
from datasheet.blocks import GridDataBlock
from teconn.blocks import FeaturesBlock, ApplicationsBlock, CarouselEmbedBlock


class SheetPageTag(TaggedItemBase):
    content_object = ParentalKey('SheetPage', related_name='sager_tagged_items')


class IndexPage(IndexBasePage):
    """
    The index or homepage of sager
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='sager_index')

    subpage_types = ['sager.SheetPage']

    class Meta:
        verbose_name = "Sager Index Page"


class SheetPage(SheetBasePage):
    """
    Subpage for sager indexpage
    """
    page_ptr = models.OneToOneField(Page, on_delete=models.CASCADE, parent_link=True,
                                    related_name='sager_sheet')

    sheet_blocks = StreamField([
        ('grid', GridDataBlock()),
    ], blank=True)

    attributes = StreamField([
        ('features', FeaturesBlock()),
        ('applications', ApplicationsBlock())
    ], blank=True)

    carousel = StreamField([
        ('embed', CarouselEmbedBlock()),
    ], blank=True)

    parent_page_types = ['sager.IndexPage']

    tags = ClusterTaggableManager(through=SheetPageTag, blank=True, related_name='sager_sheetpage_tags')

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
        max_length = 0
        for block in self.attributes:
            max_length = max(max_length, len(block.value[block.block_type]))

        context['max_length'] = max_length
        return context


class RelatedLinks(Orderable):
    page = ParentalKey(SheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
