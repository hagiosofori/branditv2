# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-27 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0039_auto_20171027_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry_comment',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
