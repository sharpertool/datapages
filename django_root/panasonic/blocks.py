import json

from datasheet.blocks import BaseBlock, JSONTextBlock
from teconn.blocks import CarouselImageBlock


class PanasonicCarouselImageBlock(CarouselImageBlock):
    class Meta:
        template = 'panasonic/blocks/_carousel_image.html'


class PartSelectorBlock(BaseBlock):
    json_data = JSONTextBlock(required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['json_data'] = json.loads(value['json_data'])
        return context

    class Meta:
        template = 'panasonic/blocks/_part_selector.html'
