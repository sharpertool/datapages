from textwrap import dedent
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from datasheet.blocks import BaseBlock


class ContactDataBlock(BaseBlock):
    """
    Block definition to capture contact data block, as seen in TE datasheet
    """
    data = TableBlock(table_options={
        'startCols': 2,
        'startRows': 1,
        'colHeaders': True,
        'editor': 'handsontable'
    })

    class Meta:
        template = 'sager/blocks/_contact_data.html'


class RevisionDataBlock(blocks.StructBlock):
    date = blocks.DateBlock()
    revisions = blocks.ListBlock(blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('description', blocks.CharBlock())
        ],
        form_template='sager/blocks/editing/common/_struct_inline.html'))


class RevisionBlock(BaseBlock):
    """
    Block definition to capture revision data, as seen in TE datasheet
    """
    data = blocks.ListBlock(RevisionDataBlock())

    class Meta:
        template = 'sager/blocks/_revision.html'
        form_classname = 'revision-block'


class FeaturesBlock(blocks.StructBlock):
    features = blocks.ListBlock(blocks.RichTextBlock(features=['bold', 'italic']))

    class Meta:
        label = 'Features'
        template = 'sager/blocks/_features_list.html'


class ApplicationsBlock(blocks.StructBlock):
    applications = blocks.ListBlock(blocks.RichTextBlock(features=['bold', 'italic']))

    class Meta:
        label = 'Applications'
        template = 'sager/blocks/_applications_list.html'


class HighlightsBlock(blocks.StructBlock):
    highlights = blocks.ListBlock(blocks.RichTextBlock(features=['bold', 'italic']))

    class Meta:
        label = 'Highlights'
        template = 'sager/blocks/_highlights_list.html'


class CarouselImageBlock(blocks.StructBlock):
    """
    Image that fits into a carousel
    """
    subtitle = blocks.CharBlock()
    image = ImageChooserBlock()
    alt = blocks.CharBlock(required=False)
    width = blocks.IntegerBlock(required=False)
    height = blocks.IntegerBlock(required=False)

    class Meta:
        template = 'sager/blocks/_carousel_image.html'


class CarouselStreamBlock(blocks.StreamBlock):
    image = CarouselImageBlock()

    class Meta:
        icon = 'cogs'


class CapacitorProductCodeItemBlock(blocks.StructBlock):
    value = blocks.CharBlock()
    options = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('key', blocks.CharBlock()),
                ('value', blocks.CharBlock())
            ],
            form_template='teconn/blocks/editing/common/_struct_inline.html'
        ),
        required=False
    )

    class Meta:
        template = 'sager/blocks/_capacitor_product_code_item.html'
        form_classname = 'product-code-block'


class CapacitorProductCodeBlock(BaseBlock):
    cde_type = CapacitorProductCodeItemBlock()
    capacitance_code = CapacitorProductCodeItemBlock()
    capacitance_tolerance = CapacitorProductCodeItemBlock()
    wvdc_code = CapacitorProductCodeItemBlock()
    packaging_code = CapacitorProductCodeItemBlock()

    class Meta:
        template = 'sager/blocks/_capacitor_product_code.html'
