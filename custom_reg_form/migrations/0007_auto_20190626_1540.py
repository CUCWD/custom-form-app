# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-06-26 19:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_reg_form', '0006_auto_20190626_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrainfo',
            name='zip',
        ),
        migrations.AddField(
            model_name='extrainfo',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Must be a valid zipcode', regex=b'^(\\d{5}([\\-]\\d{4})?)$')], verbose_name=b'Zip Code'),
        ),
    ]
