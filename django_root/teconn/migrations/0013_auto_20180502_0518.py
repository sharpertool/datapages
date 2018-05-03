# Generated by Django 2.0.4 on 2018-05-02 05:18

import datasheet.blocks
from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('teconn', '0012_auto_20180501_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetpage',
            name='sheet_blocks',
            field=wagtail.core.fields.StreamField((('contact_data', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('data', wagtail.contrib.table_block.blocks.TableBlock(table_options={'colHeaders': True, 'editor': 'handsontable', 'startCols': 2, 'startRows': 1}))))), ('coil_data', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('coils', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('name', wagtail.core.blocks.CharBlock()), ('subtitle', wagtail.core.blocks.CharBlock()), ('data_table', wagtail.contrib.table_block.blocks.TableBlock(table_options={'colHeaders': True})), ('image_title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))))))), ('dimension', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))), ('product_code', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('type', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('relay_version', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('coil_version', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('coil_system', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('load_voltage', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('contact_material', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('status_monitoring', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('coil_connector_version', wagtail.core.blocks.StructBlock((('value', wagtail.core.blocks.CharBlock()), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('key', wagtail.core.blocks.CharBlock()), ('value', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html'), required=False))))), ('code_table', wagtail.contrib.table_block.blocks.TableBlock({'colHeaders': True, 'startCols': 7, 'startRows': 1}))))), ('revisions', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('data', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('date', wagtail.core.blocks.DateBlock()), ('revisions', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock())), form_template='teconn/blocks/editing/common/_struct_inline.html')))))))))), ('characteristics', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(default='Characteristics')), ('subtitle', wagtail.core.blocks.CharBlock(require=False)), ('bookmark', wagtail.core.blocks.CharBlock(default='characteristics')), ('charts', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=False)), ('subtitle', wagtail.core.blocks.CharBlock(require=False)), ('type', wagtail.core.blocks.CharBlock(require=False)), ('legend', wagtail.core.blocks.CharBlock(required=False)), ('x_axis', wagtail.core.blocks.CharBlock(required=False)), ('y_axis', wagtail.core.blocks.CharBlock(required=False)), ('chart_values', datasheet.blocks.JSONTextBlock(required=False))))))))), ('chart', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('subtitle', wagtail.core.blocks.CharBlock(require=False)), ('type', wagtail.core.blocks.CharBlock(require=False)), ('legend', wagtail.core.blocks.CharBlock(required=False)), ('x_axis', wagtail.core.blocks.CharBlock(required=False)), ('y_axis', wagtail.core.blocks.CharBlock(required=False)), ('chart_values', datasheet.blocks.JSONTextBlock(required=False))))), ('video', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=False)), ('bookmark', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.TextBlock()))))), blank=True),
        ),
    ]