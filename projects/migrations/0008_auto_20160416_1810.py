# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-16 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.CharField(default='4/16/2015', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.CharField(default='9/30/2016', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='update_date',
            field=models.CharField(default='4/16/2016', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(max_length=60),
        ),
    ]
