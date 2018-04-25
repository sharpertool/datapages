import json

from django.core.exceptions import ValidationError

from textwrap import dedent

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock, EmbedValue


class BaseBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock()


class SelectorBlock(BaseBlock):
    json_data = blocks.CharBlock(required=False)

    class Meta:
        template = 'datasheet/blocks/_selector.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['json_data'] = json.loads(value['json_data'])
        return context

    def clean(self, value):
        results = super(SelectorBlock, self).clean(value)
        if value['json_data']:
            try:
                json.loads(value['json_data'])
            except ValueError:
                raise ValidationError('Validation error in selector block.', params={
                    'json_data': ['Must be valid json value.']
                })
        return results

class ChartBlock(BaseBlock):
    subtitle = blocks.CharBlock(require=False)
    legend = blocks.CharBlock(required=False)
    x_axis = blocks.CharBlock(required=False)
    y_axis = blocks.CharBlock(required=False)
    chart_values = blocks.CharBlock(required=False)

    class Meta:
        template = 'datasheet/blocks/_chart.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['chart_props'] = json.dumps(value)
        return context

    def clean(self, value):
        results = super(ChartBlock, self).clean(value)
        if value['chart_values']:
            try:
                json.dumps(value['chart_values'])
            except ValueError:
                raise ValidationError('Validation error in selector block.', params={
                    'json_data': ['Must be valid json value.']
                })
        return results


class DimensionBlock(BaseBlock):
    image = ImageChooserBlock()

    class Meta:
        template = 'datasheet/blocks/_dimension.html'
