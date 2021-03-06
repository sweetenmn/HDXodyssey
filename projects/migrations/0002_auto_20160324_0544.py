# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-24 05:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dept', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('project_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='projects.Project')),
                ('narrative', models.CharField(max_length=500)),
                ('created_date', models.DateTimeField(verbose_name='created on')),
                ('status', models.CharField(max_length=20)),
                ('updated_date', models.DateTimeField(verbose_name='updated on')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='advisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Advisor'),
        ),
        migrations.AddField(
            model_name='group',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.AddField(
            model_name='group',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('student', 'project')]),
        ),
    ]
