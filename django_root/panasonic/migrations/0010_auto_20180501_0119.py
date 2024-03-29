# Generated by Django 2.0.4 on 2018-05-01 01:19

import datasheet.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('panasonic', '0009_auto_20180426_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetpage',
            name='sheet_blocks',
            field=wagtail.core.fields.StreamField((('grid', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('subtitle', wagtail.core.blocks.CharBlock(required=False)), ('json_data', datasheet.blocks.JSONTextBlock(required=False))))), ('selector', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('json_data', datasheet.blocks.JSONTextBlock(required=False))))), ('dimension', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))), ('chart', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('subtitle', wagtail.core.blocks.CharBlock(require=False)), ('type', wagtail.core.blocks.CharBlock(require=False)), ('legend', wagtail.core.blocks.CharBlock(required=False)), ('x_axis', wagtail.core.blocks.CharBlock(required=False)), ('y_axis', wagtail.core.blocks.CharBlock(required=False)), ('chart_values', datasheet.blocks.JSONTextBlock(required=False))))))),
        ),
    ]
