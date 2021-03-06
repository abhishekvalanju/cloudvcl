# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-10 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvcl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flavor',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_instructor',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as an instructor.', verbose_name='instructor'),
        ),
    ]
