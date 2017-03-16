# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 02:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cvcl', '0008_auto_20170313_0142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='environmentdefinition',
            options={'verbose_name': 'Environment Definition'},
        ),
        migrations.AlterModelOptions(
            name='vm',
            options={'verbose_name': 'VM'},
        ),
        migrations.AlterModelOptions(
            name='vmdefinition',
            options={'verbose_name': 'VM Definition'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='courses',
        ),
        migrations.AddField(
            model_name='flavor',
            name='disk',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flavor',
            name='ram',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flavor',
            name='swap',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flavor',
            name='vcpus',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='cvcl.Course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='studies', to=settings.AUTH_USER_MODEL),
        ),
    ]
