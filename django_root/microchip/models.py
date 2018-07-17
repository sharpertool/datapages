import json
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (StreamFieldPanel, FieldPanel,
                                         InlinePanel, MultiFieldPanel)
from wagtail.core.models import Page, Orderable, Site

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

    def get_hierarchy_data(self):
        children = self.get_children().order_by('title')
        noprefix = lambda s: s if '::' not in s else s.partition('::')[2]
        site = Site.objects.get(hostname__startswith='microchip.datapages')

        def render(children):
            out = []
            for child in children:
                d = {
                    'name': noprefix(child.title),
                    'children': render(child.get_children().order_by('title')),
                    'url': child.get_url(current_site=site)
                }
                out.append(d)
            return out

        return {
            'name': 'root',
            'toggled': True,
            'children': render(children)
        }

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        hierarchy = self.get_hierarchy_data()
        context['hierarchy_data'] = json.dumps(hierarchy)
        return context


class SheetSubPage(Page):
    ajax_template = 'microchip/sheet_sub_page_ajax.html'

    title_raw = models.CharField(
        verbose_name=_('title_raw'),
        max_length=255,
        help_text=_("The page title as you'd like it to be seen by the public, without the prefix")
    )
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

    def full_clean(self, *args, **kwargs):
        """ build slug with title_raw, not title """

        if not self.slug:
            # Try to auto-populate slug from title
            base_slug = slugify(self.title_raw, allow_unicode=True)

            # only proceed if we get a non-empty base slug back from slugify
            if base_slug:
                self.slug = self._get_autogenerated_slug(base_slug)
                print(f"Calculated slug based on title_raw: {self.slug}")

        if not self.draft_title:
            self.draft_title = self.title_raw

        return super().full_clean(*args, **kwargs)


class RelatedLinks(Orderable):
    page = ParentalKey(SheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]
