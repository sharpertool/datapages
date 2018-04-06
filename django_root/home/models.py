from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


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
