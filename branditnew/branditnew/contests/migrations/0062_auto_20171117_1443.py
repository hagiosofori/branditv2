# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0061_print_order_is_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contests.Transaction_Status'),
        ),
    ]
