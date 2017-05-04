# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-04 04:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvcl', '0018_auto_20170503_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='vmdefinition',
            name='default_user',
            field=models.BooleanField(default=True, help_text="(Linux-only) Create a user in the system based on student's username and a random password (will be provided to student)."),
        ),
        migrations.AddField(
            model_name='vmdefinition',
            name='default_user_sudo',
            field=models.CharField(blank=True, default='ALL = (ALL) NOPASSWD: ALL', help_text="(Linux-only) Set sudo access for the student's system user. Set to 'ALL = (ALL) NOPASSWD: ALL' for unlimited sudo access.", max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vmdefinition',
            name='install_packages',
            field=models.TextField(blank=True, help_text='(Linux-only) Install packages using system package manager. One package name per line.', null=True),
        ),
        migrations.AddField(
            model_name='vmdefinition',
            name='public_key',
            field=models.CharField(blank=True, help_text='(Linux-only) SSH public key for default user (username is OS-dependant), e.g.: ssh-rsa AAAB... user@host', max_length=500, null=True),
        ),
    ]
