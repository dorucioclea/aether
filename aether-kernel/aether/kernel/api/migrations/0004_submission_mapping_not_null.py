# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-16 12:40
from __future__ import unicode_literals

from django.db import migrations


def remove_invalid_submissions(apps, schema_editor):
    Submission = apps.get_model('kernel', 'Submission')
    for submission in Submission.objects.all():
        if not submission.mapping:
            submission.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('kernel', '0003_auto_20180112_0938'),
    ]

    operations = [
        migrations.RunPython(remove_invalid_submissions, migrations.RunPython.noop),
    ]