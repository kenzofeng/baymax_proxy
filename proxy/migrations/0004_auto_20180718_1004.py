# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-18 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0003_node_aws_instance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='aws_instance_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='host',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
