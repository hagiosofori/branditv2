# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0006_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10000000, null=True),
        ),
    ]
