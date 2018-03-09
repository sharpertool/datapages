from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock, EmbedValue


class RelayProductCodeStructureBlock(blocks.StructBlock):
    """
    Capture all of the parts of a product code, somewhat specific to TE
    """
    type = blocks.CharBlock(value_class='foo bar')
    version = blocks.CharBlock()
    coil_version = blocks.CharBlock()
    coil_system = blocks.CharBlock()
    load_voltage = blocks.CharBlock()
    contact_material = blocks.CharBlock()
    status = blocks.CharBlock()
    connector_version = blocks.CharBlock()
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
    alt = blocks.CharBlock()


class CarouselEmbedBlock(blocks.StructBlock):
    """
    Embed option for the carousel
    """
    subtitle = blocks.CharBlock()
    embed = EmbedBlock()


class FeaturesBlock(blocks.StructBlock):
    subtitle = blocks.CharBlock()
    feature = blocks.ListBlock(blocks.RichTextBlock(label="feature"))

class ApplicationsBlock(blocks.StructBlock):
    subtitle = blocks.CharBlock()
    applications = blocks.ListBlock(blocks.RichTextBlock(label="application"))

class ContactDataBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    data = TableBlock({
        'startCols': 3,
        'startRows': 1,
        'colHeaders': True,
    })


class CoilDataItemBlock(blocks.StructBlock):
    """ Individual Coil Data Item """
    name = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    data_table = TableBlock({
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

