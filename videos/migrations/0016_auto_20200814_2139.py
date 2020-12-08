# Generated by Django 3.0.8 on 2020-08-14 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_auto_20200812_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='public',
            new_name='private',
        ),
        migrations.AlterField(
            model_name='channel',
            name='date_created',
            field=models.CharField(default=datetime.date(2020, 8, 14), max_length=15),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.CharField(default=datetime.date(2020, 8, 14), max_length=15),
        ),
        migrations.AlterField(
            model_name='video',
            name='published_date',
            field=models.CharField(default=datetime.date(2020, 8, 14), max_length=15),
        ),
    ]
