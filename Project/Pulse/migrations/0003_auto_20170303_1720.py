# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-03 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pulse', '0002_auto_20170302_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='hit',
            name='time_pub',
            field=models.TimeField(default='3:00:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hit',
            name='date_pub',
            field=models.DateField(),
        ),
    ]
