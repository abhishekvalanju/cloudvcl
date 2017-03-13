# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 01:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cvcl', '0004_auto_20170310_1702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['end_date']},
        ),
        migrations.AddField(
            model_name='vm',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='state',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='environment',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='environments', to='cvcl.Assignment'),
        ),
        migrations.AlterField(
            model_name='environmentdefinition',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='environment_definitions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, to='cvcl.Course'),
        ),
        migrations.AlterField(
            model_name='user',
            name='images',
            field=models.ManyToManyField(blank=True, to='cvcl.Image'),
        ),
        migrations.AlterField(
            model_name='vm',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vms', to='cvcl.Environment'),
        ),
        migrations.AlterField(
            model_name='vm',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True),
        ),
        migrations.AlterField(
            model_name='vmdefinition',
            name='user_script',
            field=models.TextField(blank=True, null=True),
        ),
    ]
