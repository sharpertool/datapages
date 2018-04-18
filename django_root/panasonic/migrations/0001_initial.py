# Generated by Django 2.0.4 on 2018-04-18 18:37

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('svglogo', models.FileField(blank=True, null=True, upload_to='')),
                ('page_logo', models.FileField(blank=True, null=True, upload_to='')),
                ('primary_color', models.CharField(default='#000', max_length=20)),
                ('secondary_color', models.CharField(default='#ddd', max_length=20)),
                ('chat_url', models.CharField(blank=True, max_length=250)),
                ('page_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='panasonic_index', serialize=False, to='wagtailcore.Page')),
                ('banner_mark', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Panasonic Index Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RelatedLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SheetPage',
            fields=[
                ('date', models.DateField(verbose_name='Post Date')),
                ('intro', models.CharField(blank=True, max_length=250)),
                ('part_number', models.CharField(blank=True, max_length=250)),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('page_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='panasonic_sheet', serialize=False, to='wagtailcore.Page')),
                ('sheet_blocks', wagtail.core.fields.StreamField((('selector', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('json_data', wagtail.core.blocks.CharBlock(required=False))))), ('dimension', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('bookmark', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()))))))),
            ],
            options={
                'verbose_name': 'Sheet Page',
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SheetPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='panasonic.SheetPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='panasonic_sheetpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sheetpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='sheetpage_tags', through='panasonic.SheetPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='relatedlinks',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='panasonic.SheetPage'),
        ),
    ]
