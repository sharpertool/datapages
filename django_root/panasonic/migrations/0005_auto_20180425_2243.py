# Generated by Django 2.0.4 on 2018-04-25 22:43

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('panasonic', '0004_auto_20180425_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetpage',
            name='sheet_blocks',
            field=wagtail.core.fields.StreamField((('selector', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('json_data', wagtail.core.blocks.CharBlock(required=False))))), ('dimension', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())))), ('chart', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('subtitle', wagtail.core.blocks.CharBlock(require=False)), ('legend', wagtail.core.blocks.CharBlock(required=False)), ('x_axis', wagtail.core.blocks.CharBlock(required=False)), ('y_axis', wagtail.core.blocks.CharBlock(required=False)), ('chart_values', wagtail.core.blocks.TextBlock(required=False))))))),
        ),
    ]
