# Generated by Django 3.0.8 on 2020-08-05 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20200805_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channelpicture',
            field=models.ImageField(default='../static/black.png', upload_to=''),
        ),
    ]
