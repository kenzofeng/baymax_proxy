# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-18 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0004_auto_20180718_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='projects',
            field=models.ManyToManyField(blank=True, to='proxy.Project'),
        ),
    ]
