# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_proposal_narrative_as_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='narrative_as_file',
        ),
        migrations.AlterField(
            model_name='proposal',
            name='narrative',
            field=models.CharField(max_length=2000),
        ),
    ]
