from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

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
        verbose_name = "Datasheet Index"

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

class DatasheetPageTag(TaggedItemBase):
    content_object = ParentalKey('DatasheetPage', related_name='tagged_items')

class DatasheetPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
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
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related Links"),
    ]


class RelatedLinks(Orderable):
    page = ParentalKey(DatasheetPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]



