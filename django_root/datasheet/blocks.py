from django import forms

from textwrap import dedent
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock, EmbedValue


class FileFieldBlock(blocks.FieldBlock):
    def __init__(self, required=True, help_text=None, max_length=None, allow_empty_file=False, **kwargs):
        self.field = forms.FileField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            allow_empty_file=allow_empty_file
        )
        print(self)
        super().__init__(**kwargs)


class DimensionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'datasheet/blocks/_dimension.html'


class RevisionDataBlock(blocks.StructBlock):
    date = blocks.DateBlock()
    revisions = blocks.ListBlock(blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('description', blocks.CharBlock())
        ],
        form_template='datasheet/blocks/editing/common/_struct_inline.html'))


class RevisionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock()
    data = blocks.ListBlock(RevisionDataBlock())

    class Meta:
        template = 'datasheet/blocks/_revision.html'
        form_classname = 'revision-block'


class ProductCodeBlock(blocks.StructBlock):
    value = blocks.CharBlock()
    options = blocks.ListBlock(
        blocks.StructBlock([
                ('key', blocks.CharBlock()),
                ('value', blocks.CharBlock())
            ],
            form_template='datasheet/blocks/editing/common/_struct_inline.html'
        ),
        required=False)

    class Meta:
        template = 'datasheet/blocks/_product_code_item.html'
        form_classname = 'product-code-block'


class RelayProductCodeStructureBlock(blocks.StructBlock):
    """
    Capture all of the parts of a product code, somewhat specific to TE
    """
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock()
    type = ProductCodeBlock()
    relay_version = ProductCodeBlock()
    coil_version = ProductCodeBlock()
    coil_system = ProductCodeBlock()
    load_voltage = ProductCodeBlock()
    contact_material = ProductCodeBlock()
    status_monitoring = ProductCodeBlock()
    coil_connector_version = ProductCodeBlock()
    code_table = TableBlock({
        'startCols': 7,
        'startRows': 1,
        'colHeaders': True,
    })

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['foo'] = "DataPages Rocks!"
        return context

    class Meta:
        icon = 'user'
        template = 'datasheet/blocks/_product_code.html'
        help_text = dedent("""
            Fill in the table with information about the Product Code.
        """)


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
        template = 'datasheet/blocks/_carousel_image.html'


class CarouselEmbedBlock(blocks.StructBlock):
    """
    Embed option for the carousel
    """
    subtitle = blocks.CharBlock()
    embed = EmbedBlock()
    width = blocks.IntegerBlock(required=False)
    height = blocks.IntegerBlock(required=False)
    allow_fullscreen = blocks.BooleanBlock(default=False)

    class Meta:
        template = 'datasheet/blocks/_carousel_embed.html'


class CarouselFusionEmbedBlock(blocks.StructBlock):
    """
    Embed option for the carousel
    """
    subtitle = blocks.CharBlock()
    embed = EmbedBlock()
    width = blocks.IntegerBlock(required=False)
    height = blocks.IntegerBlock(required=False)
    allow_fullscreen = blocks.BooleanBlock(default=False)

    class Meta:
        template = 'datasheet/blocks/_carousel_fusion_embed.html'


class CarouselStreamBlock(blocks.StreamBlock):
    image = CarouselImageBlock()
    embed = CarouselEmbedBlock()
    fusion360 = CarouselFusionEmbedBlock()

    class Meta:
        icon = 'cogs'


class FeaturesBlock(blocks.StructBlock):
    features = blocks.ListBlock(blocks.RichTextBlock(features=['bold', 'italic']))

    class Meta:
        label = 'Features'
        template = 'datasheet/blocks/_features_list.html'


class ApplicationsBlock(blocks.StructBlock):
    applications = blocks.ListBlock(blocks.RichTextBlock(features=['bold', 'italic']))

    class Meta:
        label = 'Applications'
        template = 'datasheet/blocks/_applications_list.html'


class ContactDataBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock()
    data = TableBlock(table_options={
        'startCols': 2,
        'startRows': 1,
        'colHeaders': True,
        'editor': 'handsontable'
    })

    class Meta:
        template = 'datasheet/blocks/_contact_data.html'


class CoilDataItemBlock(blocks.StructBlock):
    """ Individual Coil Data Item """
    name = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    data_table = TableBlock(table_options={
        'colHeaders': True,
    })
    image_title = blocks.CharBlock()
    image = ImageChooserBlock()


class CoilDataBlock(blocks.StructBlock):
    """
    Block definition to capture coil data, as seen in TE datasheet
    """
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock()
    coils = blocks.ListBlock(CoilDataItemBlock())

    class Meta:
        template = 'datasheet/blocks/_coil_data.html'
