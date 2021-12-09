# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-06 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_companyuser_target'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batchNumber', models.CharField(default='N/A', max_length=200)),
                ('quantity', models.FloatField(default=0.0)),
                ('rate', models.FloatField(default=0.0)),
                ('mrp', models.FloatField(default=0.0)),
                ('mDate', models.DateField(blank=True, null=True)),
                ('eDate', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('additionalDetail', models.CharField(blank=True, max_length=500, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('lastUpdatedOn', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('productID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Product')),
            ],
            options={
                'verbose_name_plural': 't) Product Batch List',
            },
        ),
        migrations.AddField(
            model_name='saleslaterproduct',
            name='batchID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.ProductBatch'),
        ),
        migrations.AddField(
            model_name='salesproduct',
            name='batchID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.ProductBatch'),
        ),
    ]