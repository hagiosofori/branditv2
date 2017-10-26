# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-25 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0034_project_submission_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_submission_comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
