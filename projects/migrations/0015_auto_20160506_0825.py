# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20160506_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completion',
            name='notation',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='narrative',
            field=models.TextField(),
        ),
    ]
