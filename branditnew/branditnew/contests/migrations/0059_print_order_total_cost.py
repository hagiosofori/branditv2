# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0058_print_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='print_order',
            name='total_cost',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
