# Generated by Django 2.0.3 on 2018-03-14 05:46

from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0016_auto_20180314_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasheetpage',
            name='stream1',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title', template='datasheet/blocks/heading.html')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('product_code', wagtail.core.blocks.StructBlock((('type', wagtail.core.blocks.CharBlock(value_class='foo bar')), ('version', wagtail.core.blocks.CharBlock()), ('coil_version', wagtail.core.blocks.CharBlock()), ('coil_system', wagtail.core.blocks.CharBlock()), ('load_voltage', wagtail.core.blocks.CharBlock()), ('contact_material', wagtail.core.blocks.CharBlock()), ('status', wagtail.core.blocks.CharBlock()), ('connector_version', wagtail.core.blocks.CharBlock()), ('code_table', wagtail.contrib.table_block.blocks.TableBlock({'colHeaders': True, 'startCols': 7, 'startRows': 1}))))), ('carousel', wagtail.core.blocks.StreamBlock((('image', wagtail.core.blocks.StructBlock((('subtitle', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('alt', wagtail.core.blocks.CharBlock(required=False))))), ('embed', wagtail.core.blocks.StructBlock((('subtitle', wagtail.core.blocks.CharBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('width', wagtail.core.blocks.IntegerBlock(required=False)), ('height', wagtail.core.blocks.IntegerBlock(required=False)), ('allow_fullscreen', wagtail.core.blocks.BooleanBlock(default=False))))), ('fusion360', wagtail.core.blocks.StructBlock((('subtitle', wagtail.core.blocks.CharBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('width', wagtail.core.blocks.IntegerBlock(required=False)), ('height', wagtail.core.blocks.IntegerBlock(required=False)), ('allow_fullscreen', wagtail.core.blocks.BooleanBlock(default=False)))))))), ('dimension', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))), ('contact_data', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('data', wagtail.contrib.table_block.blocks.TableBlock(table_options={'colHeaders': True, 'editor': 'handsontable', 'startCols': 2, 'startRows': 1}))))), ('coil_data', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('coils', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('name', wagtail.core.blocks.CharBlock()), ('subtitle', wagtail.core.blocks.CharBlock()), ('data_table', wagtail.contrib.table_block.blocks.TableBlock(table_options={'colHeaders': True})), ('image_title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))))))))),
        ),
    ]
