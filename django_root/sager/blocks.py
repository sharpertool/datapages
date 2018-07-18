from textwrap import dedent
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from datasheet.blocks import BaseBlock, JSONTextBlock


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

    def myfields(self, context=None):
        print(f"------------ Sweet.. My Fields function was called.")
        if context:
            print(f"Context is set {context}")

        return None
        # return [self.cde_type,
        #         self.capacitance_code,
        #         self.capacitance_tolerance,
        #         self.wvdc_code,
        #         self.packaging_code]

    def render(self, value, context=None):
        print(f"Rendering {value}")
        return super().render(value, context=context)


class ConfigurableProductCodeBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    bookmark = blocks.CharBlock(null=True, blank=True)
    configuration = JSONTextBlock(
        help_text=dedent("""
            JSON data structure that defines the properties for this block
            Example:
            <pre>
                { 
                  "fields": [
                    {"code": "cde", "title": "CDE"},
                    {"code": "capacitance", "title": "Capacitance (μF)"},
                    {"code": "tolerance", "title": "Tolerance (%)"},
                    {"code": "wvdc", "title": "Working Voltage (Vdc)"},
                    {"code": "packaging", "title": "Packaging"}
                  ],
                  "options": {
                    "cde": [
                        ["esrd", "ESRD"]                    
                    ],
                    "capacitance": [
                        ["4R7", "4.7 μF"],                    
                        ["220", "22 μF"],                    
                        ["101", "100 μF"]                    
                    ],
                    "tolerance": [
                        ["M", "+- 20%"]                    
                    ],
                    "wvdc": [
                        ["02", "2.0 Vdc"],                    
                        ["0E", "2.5 Vdc"],                    
                        ["04", "4.0 Vdc"],                    
                        ["06", "6.3 Vdc"]                    
                    ],
                    "packaging": [
                        ["R", "Tape & Reel"],                    
                        ["B", "Bulk"]                   
                    ]
                  }
                }
            </pre>
            """)
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update({
            'configuration': value["configuration"]
        })
        return context

    class Meta:
        template = "sager/blocks/_configurable_product_code_block.html"
