# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-06 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Feed', '0003_hit_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='negative_count',
            new_name='negative_news_count',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='positive_count',
            new_name='positive_news_count',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='total_count',
            new_name='total_news_count',
        ),
        migrations.AddField(
            model_name='company',
            name='negative_tweet_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='positive_tweet_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='total_tweet_count',
            field=models.IntegerField(default=0),
        ),
    ]
