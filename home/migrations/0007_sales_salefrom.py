# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-05-20 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_takepayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='saleFrom',
            field=models.CharField(blank=True, default='ByShop', max_length=200, null=True),
        ),
    ]
