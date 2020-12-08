# Generated by Django 3.0.8 on 2020-08-07 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20200805_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channelpicture',
            field=models.ImageField(default='../static/black.png', upload_to='channelimages/'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='date_created',
            field=models.CharField(default=datetime.date(2020, 8, 7), max_length=15),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.CharField(default=datetime.date(2020, 8, 7), max_length=15),
        ),
        migrations.AlterField(
            model_name='video',
            name='published_date',
            field=models.CharField(default=datetime.date(2020, 8, 7), max_length=15),
        ),
    ]
