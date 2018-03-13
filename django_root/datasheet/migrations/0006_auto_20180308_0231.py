# Generated by Django 2.0.3 on 2018-03-08 02:31

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0005_auto_20180306_2226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datasheetindexpage',
            options={'verbose_name': 'DataPages Index'},
        ),
        migrations.AlterField(
            model_name='datasheetpage',
            name='stream1',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('product_code', wagtail.core.blocks.StructBlock((('type', wagtail.core.blocks.CharBlock()), ('version', wagtail.core.blocks.CharBlock()), ('coil_version', wagtail.core.blocks.CharBlock()), ('coil_system', wagtail.core.blocks.CharBlock()), ('load_voltage', wagtail.core.blocks.CharBlock()), ('contact_material', wagtail.core.blocks.CharBlock()), ('status', wagtail.core.blocks.CharBlock()), ('connector_version', wagtail.core.blocks.CharBlock())))), ('carousel', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('subtitle', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('alt', wagtail.core.blocks.CharBlock()))))), ('features', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(label='feature'))))),
        ),
    ]