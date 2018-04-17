import collections
from django.db import models

from wagtail.core.models import Page, PageManager
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


from .blocks import (CarouselImageBlock, CarouselEmbedBlock, CarouselFusionEmbedBlock,
                     FeaturesBlock, ApplicationsBlock)

# ('heading', blocks.CharBlock(
#             classname="full title",
#             template="datasheet/blocks/_heading.html"
#         )),
#         ('paragraph', blocks.RichTextBlock()),
#         ('image', ImageChooserBlock()),
#         ('product_code', RelayProductCodeStructureBlock()),
#         ('carousel', CarouselStreamBlock()),
#         ('dimension', DimensionBlock()),
#         ('contact_data', ContactDataBlock()),
#         ('coil_data', CoilDataBlock()),
#         ('revisions', RevisionBlock()),
#         ('selector', SelectorBlock())


class IndexBasePage(Page):
    """
    Abstract superclass for datapage index Page.
    """
    intro = RichTextField(blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        blank=True, null=True
    )
    svglogo = models.FileField(blank=True, null=True)

    page_logo = models.FileField(blank=True, null=True)
    primary_color = models.CharField(default='#000', max_length=20)
    secondary_color = models.CharField(default='#ddd', max_length=20)
    chat_url = models.CharField(max_length=250, blank=True)
    banner_mark = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        blank=True, null=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro', classname="full"),
            FieldPanel('chat_url')
        ], heading='General Information'),
        FieldPanel('svglogo'),
        ImageChooserPanel('logo'),

        MultiFieldPanel([
            FieldPanel('page_logo'),
            FieldPanel('primary_color'),
            FieldPanel('secondary_color'),
            ImageChooserPanel('banner_mark'),
        ], heading="Sheet Page Common Values")
    ]

    subpage_types = ['SheetPage']

    @property
    def get_chat_url(self):
        return self.chat_url + '?part_number={part_number}'

    def get_context(self, request):
        context = super().get_context(request)
        context['datasheets'] = self.get_children().live().order_by('-first_published_at')
        return context

    class Meta:
        abstract = True
        verbose_name = "Index Page"


class SheetBasePage(Page):
    """
    Abstract superclass for datapage sheet Page.
    """
    date = models.DateField("Post Date")
    intro = models.CharField(max_length=250, blank=True)
    part_number = models.CharField(max_length=250, blank=True)
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

    parent_page_types = ['IndexPage']

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('part_number'),
            FieldPanel('intro'),
            FieldPanel('body', classname="full")
        ], heading="General Sheet Information"),
        MultiFieldPanel([
                StreamFieldPanel('attributes', heading=None, classname="full"),
            ],
            heading="Attributes and Applications",
            classname="collapsible collapsed"),
        StreamFieldPanel('carousel'),
    ]

    objects = PageManager()

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

        for block in self.sheet_blocks:
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
        context['chat_url'] = parent.get_chat_url.format(part_number=self.part_number)
        context['bookmarks'] = self.get_bookmarks()
        context['company_name'] = parent.title

        print(f"Logo is {parent.logo}")
        print(f"Primary Color: {parent.primary_color}")
        return context

    class Meta:
        abstract = True
        verbose_name = "Sheet Page"
