# Generated by Django 2.1.7 on 2019-03-11 12:02

import django.contrib.postgres.fields.jsonb
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid

#
# https://docs.djangoproject.com/en/2.2/topics/migrations/
#
# Once you’ve squashed your migration, you should then commit it alongside
# the migrations it replaces and distribute this change to all running
# instances of your application, making sure that they run migrate
# to store the change in their database.
#
# You must then transition the squashed migration to a normal migration by:
#
# - Deleting all the migration files it replaces.
# - Updating all migrations that depend on the deleted migrations
#   to depend on the squashed migration instead.
# - Removing the replaces attribute in the Migration class of the
#   squashed migration (this is how Django tells that it is a squashed migration).
#

if settings.MULTITENANCY:
    run_before_multitenancy = [
        ('multitenancy', '0001_initial'),
    ]
else:
    run_before_multitenancy = []


class Migration(migrations.Migration):

    initial = True

    run_before = run_before_multitenancy

    dependencies = [
    ]

    replaces = [
        ('sync', '0001_initial'),
        ('sync', '0002_devicedb_mobileuser'),
        ('sync', '0003_schema'),
        ('sync', '0004_project_artefacts'),
        ('sync', '0005_alter_meta_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='e-mail')),
            ],
            options={
                'verbose_name': 'mobile user',
                'verbose_name_plural': 'mobile users',
                'ordering': ['email'],
                'default_related_name': 'mobileusers',
            },
        ),

        migrations.CreateModel(
            name='DeviceDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.TextField(unique=True, verbose_name='device ID')),
                ('last_synced_date', models.DateTimeField(null=True, verbose_name='Last synced: date')),
                ('last_synced_seq', models.TextField(default='0', null=True, verbose_name='Last synced: sequence')),
                ('last_synced_log_message', models.TextField(null=True, verbose_name='Last synced: log message')),
                ('mobileuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='sync.MobileUser', verbose_name='mobile user')),
            ],
            options={
                'verbose_name': 'device',
                'verbose_name_plural': 'devices',
                'ordering': ['-last_synced_date'],
                'default_related_name': 'devices',
            },
        ),

        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.UUIDField(default=uuid.uuid4, help_text='This ID corresponds to an Aether Kernel project ID.', primary_key=True, serialize=False, verbose_name='project ID')),
                ('name', models.TextField(blank=True, default='', null=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
                'ordering': ['name'],
                'default_related_name': 'projects',
            },
        ),

        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, unique=True, verbose_name='name')),
                ('kernel_id', models.UUIDField(default=uuid.uuid4, help_text='This ID corresponds to an Aether Kernel Artefact ID.', verbose_name='Kernel ID')),
                ('avro_schema', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='AVRO schema')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schemas', to='sync.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'schema',
                'verbose_name_plural': 'schemas',
                'ordering': ['name'],
                'default_related_name': 'schemas',
            },
        ),
    ]
