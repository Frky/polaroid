# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 14:32


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20160323_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='path',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
