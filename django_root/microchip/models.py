import json

from django.core.cache import caches
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from wagtail.images.models import Image
from django.http import JsonResponse

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import (StreamFieldPanel, FieldPanel,
                                         InlinePanel, MultiFieldPanel)
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable, Site

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
        """
        Build a data structure that is suitable for rendeing with react treebeard

        Do not render a children: [] unless we want to dynamically load sub-sections.
        If there is a children at all, it will have an indicator for sub-levels.

        :param self:
        :return:
        """
        children = self.get_children().order_by('title')
        noprefix = lambda s: s if '::' not in s else s.partition('::')[2]
        site = Site.objects.get(hostname__startswith='microchip.datapages')
        print("Generating hierarchy data")

        def render(children):
            out = []
            for child in children:
                content = child.specific.stream.stream_data
                d = {
                    'name': noprefix(child.title),
                    'id': child.pk,
                    'slug': noprefix(child.slug),
                    'url': child.get_url(current_site=site),
                    'bookmarks': [
                        {
                            'title': stream['value']['title'],
                            'bookmark': stream['value']['bookmark']
                        }
                        for stream in content
                    ]
                }

                sub_children = child.get_children().order_by('title')
                if sub_children:
                    d.update({
                        'children': render(sub_children),
                    })

                out.append(d)
            return out

        result = render(children)
        print("Done")
        return result

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        key = "_".join([request.path, 'hierarchy_data'])
        cache = caches['default']
        hierarchy = cache.get(key)
        if hierarchy:
            print("Loaded hierarchy from cache")
        else:
            hierarchy = self.get_hierarchy_data()
            cache.set(key, hierarchy, 300)
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

    api_fields = [
        APIField('title_raw'),
        APIField('section_number'),
        APIField('pdf_page'),
        APIField('numchild'),
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['slug'] = self.slug
        context['title'] = self.title_raw
        return context

    def serve(self, request, *args, **kwargs):
        if not request.is_ajax():
            return super().serve(request, *args, **kwargs)
        else:
            has_image = lambda s: True if s.get('value').get('image', None) else False
            stream_data = []
            for stream in self.stream.stream_data:
                if has_image(stream):
                    image = stream.get('value').get('image')
                    stream_value = stream.get('value')
                    stream_value['url'] = Image.objects.get(pk=image).get_rendition('original').url
                    stream['value'] = stream_value
                stream_data.append(stream)

            return JsonResponse({
                'slug': self.slug,
                'title': self.title_raw,
                'content': stream_data
            })


class RelatedLinks(Orderable):
    page = ParentalKey(SheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]