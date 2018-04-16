# Generated by Django 2.0.3 on 2018-04-16 03:02

from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0028_datasheetindexpage_chat_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasheetpage',
            name='stream1',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title', template='datasheet/blocks/_heading.html')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('product_code', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('type', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('relay_version', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('coil_version', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('coil_system', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('load_voltage', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('contact_material', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('status_monitoring', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('coil_connector_version', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html'), required=False))))), ('code_table', wagtail.contrib.table_block.blocks.TableBlock({'colHeaders': True, 'startCols': 7, 'startRows': 1}))))), ('carousel', wagtail.core.blocks.StreamBlock((('image', wagtail.core.blocks.StructBlock((('subtitle', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('alt', wagtail.core.blocks.CharBlock(required=False)), ('width', wagtail.core.blocks.IntegerBlock(required=False)), ('height', wagtail.core.blocks.IntegerBlock(required=False))))), ('embed', wagtail.core.blocks.StructBlock((('subtitle', wagtail.core.blocks.CharBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('width', wagtail.core.blocks.IntegerBlock(required=False)), ('height', wagtail.core.blocks.IntegerBlock(required=False)), ('allow_fullscreen', wagtail.core.blocks.BooleanBlock(default=False))))), ('fusion360', wagtail.core.blocks.StructBlock((('subtitle', wagtail.core.blocks.CharBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('width', wagtail.core.blocks.IntegerBlock(required=False)), ('height', wagtail.core.blocks.IntegerBlock(required=False)), ('allow_fullscreen', wagtail.core.blocks.BooleanBlock(default=False)))))))), ('dimension', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))), ('contact_data', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('data', wagtail.contrib.table_block.blocks.TableBlock(table_options={'colHeaders': True, 'editor': 'handsontable', 'startCols': 2, 'startRows': 1}))))), ('coil_data', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('coils', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('name', wagtail.core.blocks.CharBlock()), ('subtitle', wagtail.core.blocks.CharBlock()), ('data_table', wagtail.contrib.table_block.blocks.TableBlock(table_options={'colHeaders': True})), ('image_title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))))))), ('revisions', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('data', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('date', wagtail.core.blocks.DateBlock()), ('revisions', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock())), form_template='datasheet/blocks/editing/common/_struct_inline.html')))))))))), ('selector', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('json_data', wagtail.core.blocks.CharBlock(required=False))))))),
        ),
    ]
