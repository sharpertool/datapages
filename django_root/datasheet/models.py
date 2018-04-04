import collections
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


from .blocks import (RelayProductCodeStructureBlock,
                     CarouselStreamBlock, CarouselImageBlock, CarouselEmbedBlock,
                     CarouselFusionEmbedBlock,
                     FeaturesBlock, ApplicationsBlock,
                     ContactDataBlock, CoilDataBlock, DimensionBlock, RevisionBlock
                     )

# Create your models here.
class DatasheetIndexPage(Page):
    intro = RichTextField(blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        blank=True, null=True
    )
    svglogo = models.FileField(blank=True, null=True)

    page_logo = models.FileField(blank=True, null=True)
    primary_color = models.CharField(default='#000', max_length=20)
    secondary_color = models.CharField(default='#ddd', max_length=20)
    banner_mark = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        blank=True, null=True
    )

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
        ImageChooserPanel('logo'),

        MultiFieldPanel([
            FieldPanel('page_logo'),
            FieldPanel('primary_color'),
            FieldPanel('secondary_color'),
            ImageChooserPanel('banner_mark'),
        ], heading='DataPage Common Values')
    ]


class DatasheetPageTag(TaggedItemBase):
    content_object = ParentalKey('DatasheetPage', related_name='tagged_items')


class DatasheetPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    attributes = StreamField([
        ('features', FeaturesBlock()),
        ('applications', ApplicationsBlock())
    ], blank=True)
    carousel = StreamField([
        ('image', CarouselImageBlock()),
        ('embed', CarouselEmbedBlock()),
        ('fusion360', CarouselFusionEmbedBlock()),
    ], blank=True)
    stream1 = StreamField([
        ('heading', blocks.CharBlock(
            classname="full title",
            template="datasheet/blocks/heading.html"
        )),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('product_code', RelayProductCodeStructureBlock()),
        ('carousel', CarouselStreamBlock()),
        ('dimension', DimensionBlock()),
        ('contact_data', ContactDataBlock()),
        ('coil_data', CoilDataBlock()),
        ('revisions', RevisionBlock())
    ])
    tags = ClusterTaggableManager(through=DatasheetPageTag, blank=True)

    parent_page_types = ['DatasheetIndexPage']

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="DataSheet Information"),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        MultiFieldPanel([
            StreamFieldPanel('attributes', heading=None, classname="full"),
        ],
            heading="Attributes and Applications",
            classname="collapsible collapsed"),
        StreamFieldPanel('carousel'),
        StreamFieldPanel('stream1',
                         heading='Datasheet Blocks'),
        InlinePanel('related_links', label="Related Links"),
    ]

    def get_bookmarks(self):
        """
        Iterate over the blocks and find ones that define a bookmarkk and title.
        Return turn each found bookmark as a namedtuple of id and title.

        Note: that we are just looking for StructValues here, so if the model
        is expanded to include other types that may have a bookmark, this logic will
        need to be expanded as well.

        ToDo: Extract this to a re-usable Mixin or base class so it can be re-used easier.
        :return:
        """

        Bookmark = collections.namedtuple('Bookmark', ['title', 'id'])
        bookmarks = []

        for block in self.stream1:
            val = block.value
            if isinstance(val, blocks.StructValue):
                if 'bookmark' in val and val['bookmark'] and 'title' in val:
                    bookmarks.append(Bookmark(val['title'], val['bookmark']))

        print(f"Bookmarks {bookmarks}")
        return bookmarks

    def get_context(self, request):
        context = super().get_context(request)

        parent = self.get_ancestors().last()
        parent = parent.specific

        # Add common page elements
        context['vendor_logo'] = parent.page_logo
        context['primary_color'] = parent.primary_color
        context['secondary_color'] = parent.secondary_color
        context['banner_mark'] = parent.banner_mark

        context['bookmarks'] = self.get_bookmarks()
        print(f"Logo is {parent.logo}")
        print(f"Primary Color: {parent.primary_color}")
        return context


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
