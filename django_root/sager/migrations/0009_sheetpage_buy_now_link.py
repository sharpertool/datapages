# Generated by Django 2.0.7 on 2018-07-16 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sager', '0008_auto_20180716_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetpage',
            name='buy_now_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
