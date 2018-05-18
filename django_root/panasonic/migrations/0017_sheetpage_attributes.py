# Generated by Django 2.0.3 on 2018-05-14 07:19

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('panasonic', '0016_auto_20180514_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetpage',
            name='attributes',
            field=wagtail.core.fields.StreamField((('features', wagtail.core.blocks.StructBlock((('features', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(features=['bold', 'italic']))),))), ('applications', wagtail.core.blocks.StructBlock((('applications', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(features=['bold', 'italic']))),)))), blank=True),
        ),
    ]