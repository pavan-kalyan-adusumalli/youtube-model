# Generated by Django 3.0.8 on 2020-08-20 14:24

import datetime
from django.db import migrations, models
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField 


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0016_auto_20200814_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='date_created',
            field=models.CharField(default=datetime.date(2020, 8, 20), max_length=15),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.CharField(default=datetime.date(2020, 8, 20), max_length=15),
        ),
        AlterSortedManyToManyField(
            model_name='playlist',
            name='videoname',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, related_name='playlistvideos', to='videos.Video'),
        ),
        migrations.AlterField(
            model_name='video',
            name='published_date',
            field=models.CharField(default=datetime.date(2020, 8, 20), max_length=15),
        ),
    ]
