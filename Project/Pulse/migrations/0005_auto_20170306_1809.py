# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-06 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pulse', '0004_auto_20170303_2139'),
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
        migrations.AddField(
            model_name='hit',
            name='link',
            field=models.TextField(default='www.twitter.com'),
            preserve_default=False,
        ),
    ]
