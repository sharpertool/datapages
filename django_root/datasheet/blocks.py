import json

from django.core.exceptions import ValidationError

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class BaseBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock()


class JSONTextBlock(blocks.TextBlock):
    """ Custom TextBlock for JSON data that includes a json clean function """

    def clean(self, value):
        """
        Insure we can parse the json value with loads, and then dumps it back
        to remove any excess whitespace, and store as a compact format.
        """
        value = super().clean(value)

        try:
            data = json.loads(value)
            result = json.dumps(data)
        except ValueError as e:
            error_strings = ['Chart Values json data failed to parse.']
            error_strings.extend(e.args)
            raise ValidationError('Validation error in selector block.',
                                  params={'chart_values': error_strings}
                                  )
        return result


class SelectorBlock(BaseBlock):
    json_data = JSONTextBlock(required=False)

    class Meta:
        template = 'datasheet/blocks/_selector.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['json_data'] = json.loads(value['json_data'])
        return context


class ChartBlock(BaseBlock):
    subtitle = blocks.CharBlock(require=False)
    legend = blocks.CharBlock(required=False)
    x_axis = blocks.CharBlock(required=False)
    y_axis = blocks.CharBlock(required=False)
    chart_values = JSONTextBlock(required=False)

    class Meta:
        template = 'datasheet/blocks/_chart.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['chart_values'] = value.get('chart_values', '[]').strip()
        context['chart_props'] = json.dumps(
            {k: v for k, v in value.items() if k != 'chart_values'})
        return context

    def clean(self, *args, **kwargs):
        return super().clean(*args, **kwargs)


class DimensionBlock(BaseBlock):
    image = ImageChooserBlock()

    class Meta:
        template = 'datasheet/blocks/_dimension.html'


class GridDataBlock(BaseBlock):
    subtitle = blocks.CharBlock(required=False)
    json_data = JSONTextBlock(required=False)

    class Meta:
        template = 'datasheet/blocks/_grid_data.html'
