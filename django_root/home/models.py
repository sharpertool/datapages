from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page, Site
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from datasheet.models import SiteSettings


class HomePage(Page):
    svglogo = models.FileField(blank=True)
    primary_color = models.CharField(default='#cc0000', max_length=20)
    secondary_color = models.CharField(default='#00ff00', max_length=20)

    body = RichTextField(blank=True)

    copyright = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('title'),
        FieldPanel('body', classname="full"),
        MultiFieldPanel([
            FieldPanel('svglogo'),
            FieldPanel('primary_color'),
            FieldPanel('secondary_color')
        ]),
        FieldPanel('copyright')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        settings = SiteSettings.for_site(request.site)

        parent = self.get_ancestors().last()
        parent = parent.specific

        #print(SiteSettings.for_site(parent.request))
        # Add common page elements
        context['main_logo'] = settings.logo
        context['primary_color'] = settings.primary_color
        context['secondary_color'] = settings.secondary_color
        context['banner_mark'] = settings.banner_mark
        context['company_name'] = parent.title
        context['grid_included'] = False
        context['datasheets'] = self.get_children().live().order_by('-first_published_at')
        return context
