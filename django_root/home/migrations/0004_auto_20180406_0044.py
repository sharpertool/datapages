# Generated by Django 2.0.4 on 2018-04-06 00:44

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='copyright',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='primary_color',
            field=models.CharField(default='#cc0000', max_length=20),
        ),
        migrations.AddField(
            model_name='homepage',
            name='secondary_color',
            field=models.CharField(default='#00ff00', max_length=20),
        ),
        migrations.AddField(
            model_name='homepage',
            name='svglogo',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
