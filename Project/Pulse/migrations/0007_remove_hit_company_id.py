# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-06 22:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pulse', '0006_auto_20170306_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hit',
            name='company_id',
        ),
    ]
