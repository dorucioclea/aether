# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-12 15:01
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MapFunction',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='MapResult',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('output', django.contrib.postgres.fields.jsonb.JSONField(
                    blank=True, default='{}', editable=False)),
                ('error', models.TextField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('map_function', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='core.MapFunction')),
            ],
        ),
        migrations.CreateModel(
            name='ReduceFunction',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('output', django.contrib.postgres.fields.jsonb.JSONField(
                    default='{}', editable=False)),
                ('error', models.TextField(blank=True, default='', editable=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('map_function', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='core.MapFunction')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('created_by', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('schema', django.contrib.postgres.fields.jsonb.JSONField(default='{}')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('created_by', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='core.Survey'),
        ),
        migrations.AddField(
            model_name='mapresult',
            name='response',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='core.Response'),
        ),
        migrations.AddField(
            model_name='mapfunction',
            name='survey',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='core.Survey'),
        ),
    ]