# Generated by Django 3.0.8 on 2020-08-03 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20200803_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='portfolio',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='channel',
            name='date_created',
            field=models.CharField(default=datetime.date(2020, 8, 4), max_length=15),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.CharField(default=datetime.date(2020, 8, 4), max_length=15),
        ),
        migrations.AlterField(
            model_name='video',
            name='published_date',
            field=models.CharField(default=datetime.date(2020, 8, 4), max_length=15),
        ),
    ]
