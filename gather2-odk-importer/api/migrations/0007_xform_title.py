# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_xform_form_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xform',
            name='title',
            field=models.TextField(default='', editable=False),
        ),
    ]
