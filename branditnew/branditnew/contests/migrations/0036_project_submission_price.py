# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-25 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0035_project_submission_comment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_submission',
            name='price',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]