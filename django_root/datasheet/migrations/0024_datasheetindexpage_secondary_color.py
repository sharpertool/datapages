# Generated by Django 2.0.3 on 2018-04-03 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasheet', '0023_auto_20180328_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasheetindexpage',
            name='secondary_color',
            field=models.CharField(default='#ddd', max_length=20),
        ),
    ]
