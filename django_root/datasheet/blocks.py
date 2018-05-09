import json

from django.core.exceptions import ValidationError

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

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

    type = blocks.ChoiceBlock(require=False, choices=[
        ('bar', 'Bar'),
        ('column', 'Column'),
        ('line', 'Line'),
        ('spline', 'Spline')
    ])

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

    def clean(self, value, *args, **kwargs):
        print(value)
        return super().clean(value, *args, **kwargs)


class CharacteristicsChartBlock(blocks.StructBlock):
    """ Single chart for a Chart Characteristics Block """
    title = blocks.CharBlock(required=False, default='')
    subtitle = blocks.CharBlock(require=False, default='')

    type = blocks.ChoiceBlock(require=False, choices=[
        ('bar', 'Bar'),
        ('column', 'Column'),
        ('line', 'Line'),
        ('spline', 'Spline')
    ])

    legend = blocks.CharBlock(required=False, default='')
    x_axis_config = JSONTextBlock(required=False, default='{}')
    y_axis_config = JSONTextBlock(required=False, default='{}')
    chart_values = JSONTextBlock(required=True, default='[]')

    class Meta:
        template = 'datasheet/blocks/_characteristics_chart.html'

    def get_context(self, value, parent_context=None):
        """
        Pull the chart values out and put them into context variables.
        Provide defaults, and check for empty values in the database.
        :param value:
        :param parent_context:
        :return:
        """
        context = super().get_context(value, parent_context=parent_context)

        context_keys = {
            'chart_values': '[]',
            'x_axis_config': '{}',
            'y_axis_config': '{}'
        }
        for key, default in context_keys.items():
            context[key] = value.get(key, default)
            if context[key] is None:
                context[key] = default

        context['chart_props'] = json.dumps(
            {k: v for k, v in value.items() if k not in context_keys})

        return context


class CharacteristicsBlock(blocks.StructBlock):
    """
    Characteristics Table that contains multiple
    characteristics charts in a 2-up or 1-up pattern
    """
    title = blocks.CharBlock(default="Characteristics")
    subtitle = blocks.CharBlock(require=False)
    bookmark = blocks.CharBlock(default="characteristics")
    charts = blocks.ListBlock(CharacteristicsChartBlock())

    class Meta:
        template = 'datasheet/blocks/_characteristics.html'


class DimensionBlock(BaseBlock):
    image = ImageChooserBlock()

    class Meta:
        template = 'datasheet/blocks/_dimension.html'


class GridDataBlock(BaseBlock):
    subtitle = blocks.CharBlock(required=False)
    json_data = JSONTextBlock(required=False)

    class Meta:
        template = 'datasheet/blocks/_grid_data.html'


class VideoBlock(BaseBlock):
    title = blocks.CharBlock(required=False)
    url = blocks.TextBlock()

    class Meta:
        template = 'datasheet/blocks/_video.html'


class Embed3DBlock(BaseBlock):
    uuid = blocks.CharBlock()
    share_link = blocks.TextBlock()

    class Meta:
        template = 'datasheet/blocks/_embed_3d.html'


class PDFBlock(BaseBlock):
    file = DocumentChooserBlock()
    height = blocks.IntegerBlock(default=550)
    view = blocks.ChoiceBlock(choices=[
        ('Fit', 'Fit'),
        ('FitH', 'FitH'),
        ('FitH,top', 'FitH,top'),
        ('FitV', 'FitV'),
        ('FitV,left', 'FitV,left'),
        ('FitB', 'FitB'),
        ('FitBH', 'FitBH'),
        ('FitBH,top', 'FitBH,top'),
        ('FitBV', 'FitBV'),
        ('FitBV,left', 'FitBV,left')
    ], required=False)

    class Meta:
        template = 'datasheet/blocks/_pdf.html'
