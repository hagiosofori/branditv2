# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0011_auto_20170914_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]