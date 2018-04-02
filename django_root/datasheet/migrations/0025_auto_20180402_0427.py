# Generated by Django 2.0.3 on 2018-04-02 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0024_auto_20180402_0339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasheetindexpage',
            name='page_logo',
        ),
        migrations.RemoveField(
            model_name='datasheetindexpage',
            name='svglogo',
        ),
        migrations.AddField(
            model_name='datasheetindexpage',
            name='secondary_color',
            field=models.CharField(default='#ddd', max_length=20),
        ),
    ]
