from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock, EmbedValue


class DimensionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'datasheet/blocks/dimension.html'


class RevisionBlock(blocks.StructBlock):
    date = blocks.DateBlock()
    revisions = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock()),
        ('description', blocks.CharBlock())
    ]))


class ProductCodeBlock(blocks.StructBlock):
    value = blocks.CharBlock()
    options = blocks.ListBlock(blocks.StructBlock([
        ('key', blocks.CharBlock()),
        ('value', blocks.CharBlock())
    ]))

    class Meta:
        template = 'datasheet/blocks/product_code_item.html'


class RelayProductCodeStructureBlock(blocks.StructBlock):
    """
    Capture all of the parts of a product code, somewhat specific to TE
    """
    title = blocks.CharBlock()
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
        template = 'datasheet/blocks/product_code.html'
        form_classname = "product_code struct-block"


class CarouselImageBlock(blocks.StructBlock):
    """
    Image that fits into a carousel
    """
    subtitle = blocks.CharBlock()
    image = ImageChooserBlock()
    alt = blocks.CharBlock(required=False)

    class Meta:
        template = 'datasheet/blocks/carousel_image.html'


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
        template = 'datasheet/blocks/carousel_embed.html'

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
        template = 'datasheet/blocks/carousel_fusion_embed.html'


class CarouselStreamBlock(blocks.StreamBlock):
    image = CarouselImageBlock()
    embed = CarouselEmbedBlock()
    fusion360 = CarouselFusionEmbedBlock()

    class Meta:
        icon = 'cogs'


class FeaturesBlock(blocks.StructBlock):
    features = blocks.ListBlock(blocks.RichTextBlock())

    class Meta:
        label = 'Features'
        template = 'datasheet/blocks/features_list.html'


class ApplicationsBlock(blocks.StructBlock):
    applications = blocks.ListBlock(blocks.RichTextBlock())

    class Meta:
        label = 'Applications'
        template = 'datasheet/blocks/applications_list.html'


class ContactDataBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    data = TableBlock(table_options={
        'startCols': 2,
        'startRows': 1,
        'colHeaders': True,
        'editor': 'handsontable'
    })

    class Meta:
        template = 'datasheet/blocks/contact_data.html'


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
    coils = blocks.ListBlock(CoilDataItemBlock())

    class Meta:
        template = 'datasheet/blocks/coil_data.html'


