# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vrpages', '0013_auto_20161129_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='polishurl',
            name='domain_authority',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
