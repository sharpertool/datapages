# Generated by Django 2.0.3 on 2018-04-05 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0027_datasheetpage_part_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasheetindexpage',
            name='chat_url',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]