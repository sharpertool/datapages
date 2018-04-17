from textwrap import dedent
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock

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
        template = 'teconn/blocks/_contact_data.html'


class CoilDataItemBlock(blocks.StructBlock):
    """ Individual Coil Data Item """
    name = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    data_table = TableBlock(table_options={
        'colHeaders': True,
    })
    image_title = blocks.CharBlock()
    image = ImageChooserBlock()


class CoilDataBlock(BaseBlock):
    """
    Block definition to capture coil data, as seen in TE datasheet
    """
    coils = blocks.ListBlock(CoilDataItemBlock())

    class Meta:
        template = 'teconn/blocks/_coil_data.html'


class ProductCodeBlock(blocks.StructBlock):
    value = blocks.CharBlock()
    options = blocks.ListBlock(
        blocks.StructBlock([
                ('key', blocks.CharBlock()),
                ('value', blocks.CharBlock())
            ],
            form_template='teconn/blocks/editing/common/_struct_inline.html'
        ),
        required=False)

    class Meta:
        template = 'teconn/blocks/_product_code_item.html'
        form_classname = 'product-code-block'


class RelayProductCodeStructureBlock(BaseBlock):
    """
    Capture all of the parts of a product code, somewhat specific to TE
    """
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
        template = 'teconn/blocks/_product_code.html'
        help_text = dedent("""
            Fill in the table with information about the Product Code.
        """)


class RevisionDataBlock(blocks.StructBlock):
    date = blocks.DateBlock()
    revisions = blocks.ListBlock(blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('description', blocks.CharBlock())
        ],
        form_template='teconn/blocks/editing/common/_struct_inline.html'))


class RevisionBlock(BaseBlock):
    """
    Block definition to capture revision data, as seen in TE datasheet
    """
    data = blocks.ListBlock(RevisionDataBlock())

    class Meta:
        template = 'teconn/blocks/_revision.html'
        form_classname = 'revision-block'