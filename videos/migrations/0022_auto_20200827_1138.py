# Generated by Django 3.0.8 on 2020-08-27 06:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0021_auto_20200826_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='date_created',
            field=models.CharField(default=datetime.date(2020, 8, 27), max_length=15),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.CharField(default=datetime.date(2020, 8, 27), max_length=15),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='channelname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='channelplaylists', to='videos.Channel'),
        ),
        migrations.AlterField(
            model_name='video',
            name='published_date',
            field=models.CharField(default=datetime.date(2020, 8, 27), max_length=15),
        ),
    ]
