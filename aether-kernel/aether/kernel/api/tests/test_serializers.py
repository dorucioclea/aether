# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import copy
import uuid

from django.test import RequestFactory, TestCase
from rest_framework.serializers import ValidationError

from aether.kernel.api import models, serializers

from . import EXAMPLE_SCHEMA, EXAMPLE_SOURCE_DATA, EXAMPLE_SOURCE_DATA_ENTITY, EXAMPLE_MAPPING


class SerializersTests(TestCase):

    def setUp(self):
        super(SerializersTests, self).setUp()
        self.request = RequestFactory().get('/')

    def test__serializers__create_and_update(self):

        project = serializers.ProjectSerializer(
            data={
                'name': 'a project name',
            },
            context={'request': self.request},
        )
        self.assertTrue(project.is_valid(), project.errors)
        project.save()

        # check schema with definition validation
        schema = serializers.SchemaSerializer(
            data={
                'name': 'a schema name',
                'definition': {},
            },
            context={'request': self.request},
        )
        self.assertFalse(schema.is_valid(), schema.errors)
        self.assertIn('No "type" property', schema.errors['definition'][0])

        schema = serializers.SchemaSerializer(
            data={
                'name': 'a schema name',
                'definition': {
                    'type': 'record',
                },
            },
            context={'request': self.request},
        )
        self.assertFalse(schema.is_valid(), schema.errors)
        self.assertIn('Record schema requires a non-empty fields property.',
                      schema.errors['definition'][0])

        schema = serializers.SchemaSerializer(
            data={
                'name': 'a schema name',
                'definition': {
                    'name': 'Test',
                    'type': 'record',
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'string',
                        }
                    ]
                },
            },
            context={'request': self.request},
        )
        self.assertFalse(schema.is_valid(), schema.errors)
        self.assertIn('A schema is required to have a field "id" of type "string"',
                      schema.errors['definition'][0])

        schema = serializers.SchemaSerializer(
            data={
                'name': 'a schema name',
                'definition': {
                    'name': 'Test',
                    'type': 'record',
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'string',
                        }
                    ]
                },
            },
            context={'request': self.request},
        )
        self.assertFalse(schema.is_valid(), schema.errors)
        self.assertIn('A schema is required to have a field "id" of type "string"',
                      schema.errors['definition'][0])

        schema = serializers.SchemaSerializer(
            data={
                'name': 'a schema name',
                'definition': EXAMPLE_SCHEMA,
            },
            context={'request': self.request},
        )
        self.assertTrue(schema.is_valid(), schema.errors)
        schema.save()

        schemadecorator = serializers.SchemaDecoratorSerializer(
            data={
                'name': 'a schema decorator name',
                'project': project.data['id'],
                'schema': schema.data['id'],
            },
            context={'request': self.request},
        )
        self.assertTrue(schemadecorator.is_valid(), schemadecorator.errors)
        schemadecorator.save()

        mappingset = serializers.MappingSetSerializer(
            data={
                'name': 'a sample mapping set',
                'project': project.data['id'],
            },
            context={'request': self.request},
        )
        self.assertTrue(mappingset.is_valid(), mappingset.errors)
        mappingset.save()

        # check mapping with definition validation
        mapping = serializers.MappingSerializer(
            data={
                'name': 'a sample mapping',
                'definition': {
                    'entities': [],  # this must be a dict
                    'mapping': {},   # this must be a list
                },
                'mappingset': mappingset.data['id'],
                'project': project.data['id'],
            },
            context={'request': self.request},
        )
        self.assertFalse(mapping.is_valid(), mapping.errors)
        self.assertIn('is not valid under any of the given schemas',
                      mapping.errors['definition'][0])

        mapping_definition = copy.deepcopy(EXAMPLE_MAPPING)
        mapping_definition['entities']['Person'] = schemadecorator.data['id']
        mapping = serializers.MappingSerializer(
            data={
                'name': 'a sample mapping',
                'definition': mapping_definition,
                'mappingset': mappingset.data['id'],
                'project': project.data['id'],
            },
            context={'request': self.request},
        )
        self.assertTrue(mapping.is_valid(), mapping.errors)
        mapping.save()

        # check the submission with entity extraction errors
        submission = serializers.SubmissionSerializer(
            data={
                'mappingset': mappingset.data['id'],
                'project': project.data['id'],
                'payload': {},  # error
            },
            context={'request': self.request},
        )
        self.assertTrue(submission.is_valid(), submission.errors)

        # save the submission and check that no entities were created
        # and we have aether errors
        self.assertEqual(models.Entity.objects.count(), 0)
        submission.save()
        self.assertEqual(models.Entity.objects.count(), 0)
        self.assertIn('aether_errors', submission.data['payload'])

        # check the submission without entity extraction errors
        submission = serializers.SubmissionSerializer(
            data={
                'mappingset': mappingset.data['id'],
                'project': project.data['id'],
                'payload': EXAMPLE_SOURCE_DATA,
            },
            context={'request': self.request},
        )
        self.assertTrue(submission.is_valid(), submission.errors)

        # save the submission and check that the entities were created
        self.assertEqual(models.Entity.objects.count(), 0)
        submission.save()
        self.assertNotEqual(models.Entity.objects.count(), 0)
        self.assertIn('aether_extractor_enrichment', submission.data['payload'])

        # check entity
        entity = serializers.EntitySerializer(
            data={
                'merge': 'overwrite',  # ignore in `create`
                'submission': submission.data['id'],
                'schemadecorator': schemadecorator.data['id'],
                'status': 'Pending Approval',
                'payload': EXAMPLE_SOURCE_DATA,  # has no id
            },
            context={'request': self.request},
        )
        self.assertTrue(entity.is_valid(), entity.errors)

        with self.assertRaises(Exception) as ve:
            entity.save()
        self.assertIn('Extracted record did not conform to registered schema',
                      str(ve.exception))

        # create entity
        entity_2 = serializers.EntitySerializer(
            data={
                'submission': submission.data['id'],
                'schemadecorator': schemadecorator.data['id'],
                'mapping': mapping.data['id'],
                'status': 'Pending Approval',
                'payload': EXAMPLE_SOURCE_DATA_ENTITY,
            },
            context={'request': self.request},
        )
        self.assertTrue(entity_2.is_valid(), entity_2.errors)
        entity_2.save()

        # update entity
        entity_3 = serializers.EntitySerializer(
            models.Entity.objects.get(pk=entity_2.data['id']),
            data={
                **entity_2.data,
                'merge': 'last_write_wins',
                'status': 'Publishable',
                'payload': {'id': 1},  # wrong id type
            },
            context={'request': self.request},
        )
        self.assertTrue(entity_3.is_valid(), entity_3.errors)

        with self.assertRaises(Exception) as ve_3:
            entity_3.save()
        self.assertIn('Extracted record did not conform to registered schema',
                      str(ve_3.exception))

        entity_4 = serializers.EntitySerializer(
            models.Entity.objects.get(pk=entity_2.data['id']),
            data={
                **entity_2.data,
                'merge': 'overwrite',
                'status': 'Publishable',
                'payload': EXAMPLE_SOURCE_DATA_ENTITY,
            },
            context={'request': self.request},
        )
        self.assertTrue(entity_4.is_valid(), entity_4.errors)
        entity_4.save()
        self.assertEqual(entity_2.data['id'], entity_4.data['id'])

        # bulk create

        # bad bulk entity
        bad_bulk = serializers.EntitySerializer(
            data=[{
                'schemadecorator': schemadecorator.data['id'],
                'status': 'Pending Approval',
                'payload': {'bad': 'entity'}
            }],
            many=True,
            context={'request': self.request},
        )
        self.assertTrue(bad_bulk.is_valid(), bad_bulk.errors)
        try:
            bad_bulk.save()
            self.assertTrue(False), 'This should have raised a ValidationError'
        except ValidationError:
            self.assertTrue(True)

        # good bulk

        create_count = 6
        # make objects
        payloads = [EXAMPLE_SOURCE_DATA_ENTITY for i in range(create_count)]
        for pl in payloads:
            pl.update({'id': str(uuid.uuid4())})
        data = [
            {
                'schemadecorator': schemadecorator.data['id'],
                'status': 'Pending Approval',
                'payload': pl
            } for pl in payloads
        ]
        # submit at once
        bulk_entities = serializers.EntitySerializer(
            data=data,
            many=True,
            context={'request': self.request},
        )
        self.assertTrue(bulk_entities.is_valid(), bulk_entities.errors)
        bulk_entities.save()
