# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-18 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0031_contest_is_touched'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='num_submissions',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
