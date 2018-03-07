from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet

# Create your models here.
class DatasheetIndexPage(Page):
    intro = RichTextField(blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        blank=True, null=True
    )
    svglogo = models.FileField(blank=True, null=True)

    subpage_types = ['DatasheetPage']

    class Meta:
        verbose_name = "DataPages Index"

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(DatasheetIndexPage, self).get_context(request)
        datasheets = self.get_children().live().order_by('-first_published_at')
        context['datasheets'] = datasheets
        return context


    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('svglogo'),
        ImageChooserPanel('logo')
    ]


## Blocks
class RelayProductCodeStructureBlock(blocks.StructBlock):
    type = blocks.CharBlock()
    version = blocks.CharBlock()
    coil_version = blocks.CharBlock()
    coil_system = blocks.CharBlock()
    load_voltage = blocks.CharBlock()
    contact_material = blocks.CharBlock()
    status = blocks.CharBlock()
    connector_version = blocks.CharBlock()

    class Meta:
        icon = 'user'

class DatasheetPageTag(TaggedItemBase):
    content_object = ParentalKey('DatasheetPage', related_name='tagged_items')

class DatasheetPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    stream1 = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('product_code', RelayProductCodeStructureBlock())
    ])
    tags = ClusterTaggableManager(through=DatasheetPageTag, blank=True)

    parent_page_types = ['DatasheetIndexPage']

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('intro'),
        InlinePanel('features', label="Features"),
        FieldPanel('body', classname="full"),
        StreamFieldPanel('stream1'),
        InlinePanel('related_links', label="Related Links"),
    ]


class Features(Orderable):
    page = ParentalKey(DatasheetPage, related_name='features')
    feature = RichTextField()

    panels = [
        FieldPanel('feature', classname="full")
    ]

class Revisions(Orderable):
    date = models.DateField()


class RelatedLinks(Orderable):
    page = ParentalKey(DatasheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]



