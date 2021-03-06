# Generated by Django 2.1.7 on 2019-03-11 11:52

import aether.kernel.api.models
import aether.kernel.api.validators
import django.contrib.postgres.fields.jsonb
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
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
        ('kernel', '0001_initial'),
        ('kernel', '0002_auto_20171218_0854'),
        ('kernel', '0003_auto_20180112_0938'),
        ('kernel', '0004_submission_mapping_not_null'),
        ('kernel', '0005_auto_20180116_1246'),
        ('kernel', '0006_auto_20180122_1346'),
        ('kernel', '0007_auto_20180208_0928'),
        ('kernel', '0008_auto_20180208_0933'),
        ('kernel', '0009_auto_20180220_1058'),
        ('kernel', '0010_auto_20180305_1540'),
        ('kernel', '0011_auto_20180524_1303'),
        ('kernel', '0012_auto_20180524_1553'),
        ('kernel', '0013_auto_20180530_1411'),
        ('kernel', '0014_remove_submission_date'),
        ('kernel', '0015_auto_20180725_1310'),
        ('kernel', '0016_auto_20180907_1214'),
        ('kernel', '0017_mappingset_schema'),
        ('kernel', '0018_schema_family'),
        ('kernel', '0019_verbose_name'),
        ('kernel', '0020_entity_schema'),
        ('kernel', '0021_auto_20181023_0711'),
        ('kernel', '0022_entity_created'),
        ('kernel', '0023_project_schema_cascade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.TextField(default='1', verbose_name='revision')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('salad_schema', models.TextField(blank=True, help_text='Semantic Annotations for Linked Avro Data (SALAD)  https://www.commonwl.org/draft-3/SchemaSalad.html', null=True, verbose_name='salad schema')),
                ('jsonld_context', models.TextField(blank=True, help_text='JSON for Linking Data  https://json-ld.org/', null=True, verbose_name='JSON LD context')),
                ('rdf_definition', models.TextField(blank=True, help_text='Resource Description Framework  https://www.w3.org/TR/rdf-schema/', null=True, verbose_name='RDF definition')),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
                'ordering': ['-modified'],
                'default_related_name': 'projects',
            },
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['-modified'], name='kernel_proj_modifie_02889d_idx'),
        ),

        migrations.CreateModel(
            name='MappingSet',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.TextField(default='1', verbose_name='revision')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('schema', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, validators=[aether.kernel.api.validators.validate_avro_schema], verbose_name='AVRO schema')),
                ('input', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='input sample')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappingsets', to='kernel.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'mapping set',
                'verbose_name_plural': 'mapping sets',
                'ordering': ['project__id', '-modified'],
                'default_related_name': 'mappingsets',
            },
        ),
        migrations.AddIndex(
            model_name='mappingset',
            index=models.Index(fields=['project', '-modified'], name='kernel_mapp_project_73242f_idx'),
        ),
        migrations.AddIndex(
            model_name='mappingset',
            index=models.Index(fields=['-modified'], name='kernel_mapp_modifie_46a12a_idx'),
        ),

        migrations.CreateModel(
            name='Submission',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.TextField(default='1', verbose_name='revision')),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='payload')),
                ('mappingset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='kernel.MappingSet', verbose_name='mapping set')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='kernel.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'submission',
                'verbose_name_plural': 'submissions',
                'ordering': ['project__id', '-modified'],
                'default_related_name': 'submissions',
            },
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(fields=['project', '-modified'], name='kernel_subm_project_3c72d6_idx'),
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(fields=['-modified'], name='kernel_subm_modifie_a4d81e_idx'),
        ),

        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='filename')),
                ('attachment_file', models.FileField(upload_to=aether.kernel.api.models.__attachment_path__, verbose_name='file')),
                ('md5sum', models.CharField(blank=True, max_length=36, verbose_name='file MD5')),
                ('submission_revision', models.TextField(verbose_name='submission revision')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='kernel.Submission', verbose_name='submission')),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
                'ordering': ['submission__id', 'name'],
                'default_related_name': 'attachments',
            },
        ),
        migrations.AddIndex(
            model_name='attachment',
            index=models.Index(fields=['submission', 'name'], name='kernel_atta_submiss_58224b_idx'),
        ),

        migrations.CreateModel(
            name='Schema',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.TextField(default='1', verbose_name='revision')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('type', models.CharField(default='org.ehealthafrica.aether', max_length=50, verbose_name='schema type')),
                ('definition', django.contrib.postgres.fields.jsonb.JSONField(validators=[aether.kernel.api.validators.validate_schema_definition], verbose_name='AVRO schema')),
                ('family', models.TextField(blank=True, null=True, verbose_name='schema family')),
            ],
            options={
                'verbose_name': 'schema',
                'verbose_name_plural': 'schemas',
                'ordering': ['-modified'],
                'default_related_name': 'schemas',
            },
        ),
        migrations.AddIndex(
            model_name='schema',
            index=models.Index(fields=['-modified'], name='kernel_sche_modifie_fc1ee1_idx'),
        ),

        migrations.CreateModel(
            name='ProjectSchema',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('mandatory_fields', models.TextField(blank=True, null=True, verbose_name='mandatory fields')),
                ('transport_rule', models.TextField(blank=True, null=True, verbose_name='transport rule')),
                ('masked_fields', models.TextField(blank=True, null=True, verbose_name='masked fields')),
                ('is_encrypted', models.BooleanField(default=False, verbose_name='encrypted?')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectschemas', to='kernel.Project', verbose_name='project')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectschemas', to='kernel.Schema', verbose_name='schema')),
            ],
            options={
                'verbose_name': 'project schema',
                'verbose_name_plural': 'project schemas',
                'ordering': ['project__id', '-modified'],
                'default_related_name': 'projectschemas',
            },
        ),
        migrations.AddIndex(
            model_name='projectschema',
            index=models.Index(fields=['project', '-modified'], name='kernel_proj_project_2dfa87_idx'),
        ),
        migrations.AddIndex(
            model_name='projectschema',
            index=models.Index(fields=['-modified'], name='kernel_proj_modifie_3ecab4_idx'),
        ),

        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.TextField(default='1', verbose_name='revision')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('definition', django.contrib.postgres.fields.jsonb.JSONField(validators=[aether.kernel.api.validators.validate_mapping_definition], verbose_name='mapping rules')),
                ('is_active', models.BooleanField(default=True, verbose_name='active?')),
                ('is_read_only', models.BooleanField(default=False, verbose_name='read only?')),
                ('mappingset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='kernel.MappingSet', verbose_name='mapping set')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='kernel.Project', verbose_name='project')),
                ('projectschemas', models.ManyToManyField(blank=True, editable=False, related_name='mappings', to='kernel.ProjectSchema', verbose_name='project schemas')),
            ],
            options={
                'verbose_name': 'mapping',
                'verbose_name_plural': 'mappings',
                'ordering': ['project__id', '-modified'],
                'default_related_name': 'mappings',
            },
        ),
        migrations.AddIndex(
            model_name='mapping',
            index=models.Index(fields=['project', '-modified'], name='kernel_mapp_project_0cb3fd_idx'),
        ),
        migrations.AddIndex(
            model_name='mapping',
            index=models.Index(fields=['-modified'], name='kernel_mapp_modifie_8c7640_idx'),
        ),

        migrations.CreateModel(
            name='Entity',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.TextField(default='1', verbose_name='revision')),
                ('modified', models.CharField(editable=False, max_length=100, verbose_name='modified')),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='payload')),
                ('status', models.CharField(choices=[('Pending Approval', 'Pending Approval'), ('Publishable', 'Publishable')], max_length=20, verbose_name='status')),
                ('mapping_revision', models.TextField(blank=True, null=True, verbose_name='mapping revision')),
                ('mapping', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entities', to='kernel.Mapping', verbose_name='mapping')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='kernel.Project', verbose_name='project')),
                ('projectschema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='kernel.ProjectSchema', verbose_name='project schema')),
                ('schema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='kernel.Schema', verbose_name='schema')),
                ('submission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entities', to='kernel.Submission', verbose_name='submission')),
            ],
            options={
                'verbose_name': 'entity',
                'verbose_name_plural': 'entities',
                'ordering': ['project__id', '-modified'],
                'default_related_name': 'entities',
            },
        ),
        migrations.AddIndex(
            model_name='entity',
            index=models.Index(fields=['project', '-modified'], name='kernel_enti_project_5d5f1b_idx'),
        ),
        migrations.AddIndex(
            model_name='entity',
            index=models.Index(fields=['-modified'], name='kernel_enti_modifie_c49ec3_idx'),
        ),
    ]
