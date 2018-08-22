import collections
import uuid
import json
from django.db import models

from wagtail.core.models import Page, PageManager, Site
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.core.models import Site
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .blocks import CharacteristicsBlock, GridDataBlock
from panasonic.blocks import PartSelectorBlock


@register_setting
class SiteSettings(BaseSetting):
    primary_color = models.CharField(default='#000', max_length=20)
    secondary_color = models.CharField(default='#ddd', max_length=20)
    logo = models.FileField(blank=True, null=True)
    banner_mark = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',
        blank=True, null=True
    )
    chat_url = models.CharField(max_length=250, blank=True)
    tile_background_color = models.CharField(default='#000', max_length=20)
    active_area_background_color = models.CharField(default='#ddd', max_length=20)
    ga_tracking_id = models.CharField(blank=True, null=True, max_length=200)
    is_distributor = models.BooleanField(default=False)

    # For content height setting
    mobile = models.CharField(blank=True, null=True, max_length=50)
    desktop = models.CharField(blank=True, null=True, max_length=50)
    tablet = models.CharField(blank=True, null=True, max_length=50)

    panels = [
        FieldPanel('primary_color'),
        FieldPanel('secondary_color'),
        FieldPanel('tile_background_color'),
        FieldPanel('active_area_background_color'),
        FieldPanel('logo'),
        ImageChooserPanel('banner_mark'),
        FieldPanel('chat_url'),
        FieldPanel('ga_tracking_id'),
        FieldPanel('is_distributor', heading="Is this a distributor?"),
        MultiFieldPanel([
            FieldPanel('mobile'),
            FieldPanel('desktop'),
            FieldPanel('tablet')
        ], heading="Content Height")
    ]

    @property
    def get_chat_url(self):
        return self.chat_url + '?part_number={part_number}'


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

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro', classname="full"),
        ], heading='General Information'),
        FieldPanel('svglogo'),
        ImageChooserPanel('logo')
    ]

    subpage_types = ['SheetPage']

    @property
    def settings(self):
        if Site.objects.filter(root_page=self).exists():
            site = Site.objects.get(root_page=self)
            return SiteSettings.for_site(site)
        return None

    def get_context(self, request):
        context = super().get_context(request)
        settings = SiteSettings.for_site(request.site)
        main_site = Site.objects.get(is_default_site=True)
        main_site_settings = SiteSettings.for_site(main_site)

        parent = self.get_ancestors().last()
        parent = parent.specific

        #print(SiteSettings.for_site(parent.request))
        # Add common page elements
        context['default_site_url'] = main_site.root_url
        context['main_logo'] = main_site_settings.logo
        context['vendor_logo'] = settings.logo
        context['primary_color'] = settings.primary_color
        context['secondary_color'] = settings.secondary_color
        context['banner_mark'] = settings.banner_mark
        context['ga_tracking_id'] = settings.ga_tracking_id
        context['company_name'] = parent.title
        context['grid_included'] = False
        context['datasheets'] = self.get_children().live().order_by('-first_published_at')

        print(f"Logo is {settings.logo}")
        print(f"Primary Color: {settings.primary_color}")
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

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    subtitle = models.CharField(max_length=250, blank=True)
    main_image = models.FileField(blank=True, null=True)

    buy_now_link = models.CharField(max_length=255, null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('part_number'),
            FieldPanel('intro'),
            FieldPanel('subtitle'),
            FieldPanel('main_image'),
            FieldPanel('body', classname="full"),
            FieldPanel('buy_now_link'),
        ], heading="General Sheet Information")
    ]

    objects = PageManager()

    def get_bookmarks(self):
        """
        Iterate over the blocks and find ones that define a bookmark and title.
        Return turn each found bookmark as a namedtuple of id and title.

        Note: that we are just looking for StructValues here, so if the model
        is expanded to include other types that may have a bookmark, this logic will
        need to be expanded as well.

        ToDo: Extract this to a re-usable Mixin or base class so it can be re-used easier.
        :return:
        """
        bookmark_ids = set(['bookmark_introduction'])

        def make_unique(bookmark, prefix='bookmark'):
            """ Append unique suffix until bookmark is unique """
            btest = f"{prefix}_{bookmark}"
            while btest in bookmark_ids:
                btest = f"{prefix}_{bookmark}_{str(uuid.uuid4())[:4]}"

            bookmark_ids.add(btest)
            return btest

        Bookmark = collections.namedtuple('Bookmark', ['title', 'id'])
        bookmarks = []

        for block in self.sheet_blocks:
            val = block.value
            if isinstance(val, blocks.StructValue):
                if 'bookmark' in val and val['bookmark'] and 'title' in val:
                    val['bookmark'] = make_unique(val['bookmark'])
                    bookmarks.append(Bookmark(val['title'], val['bookmark']))

        return bookmarks

    def get_context(self, request):
        context = super().get_context(request)
        max_length = 0
        settings = SiteSettings.for_site(request.site)
        parent = self.get_ancestors().last()
        parent = parent.specific


        # Add common page elements
        context['vendor_logo'] = settings.logo
        context['primary_color'] = settings.primary_color
        context['secondary_color'] = settings.secondary_color
        context['banner_mark'] = settings.banner_mark
        context['chat_url'] = settings.get_chat_url.format(part_number=self.part_number)
        context['bookmarks'] = self.get_bookmarks()
        context['ga_tracking_id'] = settings.ga_tracking_id
        context['is_distributor'] = settings.is_distributor
        context['company_name'] = parent.title
        context['grid_included'] = False
        context['content_height'] = json.dumps({
            "mobile": settings.mobile,
            "desktop": settings.desktop,
            "tablet": settings.tablet
        })

        for value in self.sheet_blocks:
            if isinstance(value.block, (GridDataBlock, PartSelectorBlock)):
                context['grid_included'] = True
                break

        #max_length for all sheets
        for block in self.attributes:
            max_length = max(max_length, len(block.value[block.block_type]))
            context['max_length'] = max_length

        print(f"Logo is {settings.logo}")
        print(f"Primary Color: {settings.primary_color}")
        return context

    class Meta:
        abstract = True
        verbose_name = "Sheet Page"
