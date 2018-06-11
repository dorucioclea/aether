# Copyright (C) 2018 by eHealth Africa : http://www.eHealthAfrica.org
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

import uuid

from django.db.utils import IntegrityError
from django.test import TestCase

from ..models import Project, Schema, ProjectSchema, Mapping
from ..project_artefacts import (
    get_project_artefacts as retrieve,
    upsert_project_artefacts as generate,
    __upsert_instance as upsert,
)


class ProjectArtefactsTests(TestCase):

    def test__upsert_item(self):
        # creates it with no id
        project_0 = upsert(Project, pk=None, ignore_fields=[], name='Project None', unknown=2)

        self.assertIsNotNone(project_0)
        self.assertIsNotNone(project_0.pk)
        self.assertEqual(project_0.name, 'Project None')

        _id = uuid.uuid4()

        # creates it with id
        project_1 = upsert(Project, pk=str(_id), ignore_fields=['revision'],
                           name='Project test', revision='2')

        self.assertIsNotNone(project_1)
        self.assertEqual(project_1.pk, _id)
        self.assertEqual(project_1.name, 'Project test')
        self.assertEqual(project_1.revision, '2', 'accepts revision value if creates the object')

        # updates it
        project_2 = upsert(Project, pk=_id, ignore_fields=['revision'],
                           name='Project test 2', revision='Z')

        self.assertIsNotNone(project_2)
        self.assertEqual(project_2.pk, _id)
        self.assertEqual(project_2.name, 'Project test 2')
        self.assertEqual(project_2.revision, '2', 'ignores new revision value if updates the object')

        # creates with foreign keys
        mapping_0 = upsert(Mapping, pk=None, ignore_fields=[],
                           name='Mapping None', project=project_1, definition={})

        self.assertIsNotNone(mapping_0)
        self.assertIsNotNone(mapping_0.pk)
        self.assertEqual(mapping_0.name, 'Mapping None')
        self.assertEqual(mapping_0.project, project_2)

        # updates indicated fields, keeps the rest
        mapping_1 = upsert(Mapping, pk=mapping_0.pk, ignore_fields=['name'],
                           definition={'mapping': []}, unknown=True)
        self.assertEqual(mapping_1.pk, mapping_0.pk)
        self.assertEqual(mapping_1.name, 'Mapping None')
        self.assertEqual(mapping_1.project, project_1)
        self.assertEqual(mapping_1.definition, {'mapping': []})

    def test__upsert_project_artefacts__project(self):

        # creates the project if there is no project with that id
        project_id = str(uuid.uuid4())
        self.assertEqual(Project.objects.filter(pk=project_id).count(), 0)

        results = generate(project_id=project_id)

        self.assertEqual(results['project'], str(project_id))
        self.assertEqual(results['schemas'], set())
        self.assertEqual(results['project_schemas'], set())
        self.assertEqual(results['mappings'], set())

        new_project = Project.objects.get(pk=project_id)
        self.assertIsNotNone(new_project.name)

        # creates the project if no id indicated
        results = generate(project_name='New project')

        self.assertIsNotNone(results['project'])
        self.assertEqual(results['schemas'], set())
        self.assertEqual(results['project_schemas'], set())
        self.assertEqual(results['mappings'], set())

        project = Project.objects.get(pk=results['project'])
        self.assertEqual(project.name, 'New project')

        results_retrieve = retrieve(project=project)
        self.assertEqual(results, results_retrieve)

        results = generate(project_id=project.pk, project_name='Something new')

        project.refresh_from_db()
        self.assertEqual(results['project'], str(project.pk))
        self.assertEqual(results['schemas'], set())
        self.assertEqual(results['project_schemas'], set())
        self.assertEqual(results['mappings'], set())
        self.assertEqual(project.name, 'New project', 'name is not updated')

    def test__upsert_project_artefacts__schemas(self):
        project = Project.objects.create(name='Project')
        schema_id = str(uuid.uuid4())

        results_1 = generate(project_id=project.pk, project_name=project.name, schemas=[
            {'id': schema_id, 'name': 'Schema', 'definition': {}},
        ])
        results_retrieve = retrieve(project=project)
        self.assertEqual(results_1, results_retrieve)

        self.assertEqual(results_1['project'], str(project.pk))
        self.assertEqual(results_1['schemas'], set([schema_id]))
        self.assertEqual(len(results_1['project_schemas']), 1)
        self.assertEqual(results_1['mappings'], set())

        project_schema_id = list(results_1['project_schemas'])[0]

        schema = Schema.objects.get(pk=schema_id)
        self.assertEqual(schema.name, 'Schema')
        self.assertEqual(schema.revision, '1')
        self.assertEqual(schema.definition, {})

        project_schema = ProjectSchema.objects.get(pk=project_schema_id)
        self.assertEqual(project_schema.project, project)
        self.assertEqual(project_schema.schema, schema)

        results_2 = generate(project_id=project.pk, project_name=project.name, schemas=[
            # in this case nothing changes
            {'id': schema_id, 'name': 'Schema 2'},
        ])
        self.assertEqual(results_1, results_2, 'it does no generate a new project schema')

        schema.refresh_from_db()
        self.assertEqual(schema.name, 'Schema')
        self.assertEqual(schema.revision, '1')
        self.assertEqual(schema.definition, {})

        # delete project schema
        project_schema.delete()
        results_3 = generate(project_id=project.pk, project_name=project.name, schemas=[
            # in this case the definition is updated and the deleted project schema re-generated
            {'id': schema_id, 'definition': {'name': 'Schema'}},
        ])
        self.assertNotEqual(results_1, results_3, 'generates a new project schema')
        self.assertEqual(results_3['project'], str(project.pk))
        self.assertEqual(results_3['schemas'], set([schema_id]))
        self.assertEqual(len(results_3['project_schemas']), 1)
        self.assertEqual(results_3['mappings'], set())

        schema.refresh_from_db()
        self.assertEqual(schema.name, 'Schema')
        self.assertEqual(schema.revision, '1')
        self.assertEqual(schema.definition, {'name': 'Schema'})

        # creating a new empt schema
        results_4 = generate(project_id=project.pk, project_name=project.name, schemas=[
            # It's possible to create empty schemas!!!
            {},
        ])
        self.assertNotEqual(results_1, results_4, 'only returns the affected ids')
        self.assertEqual(len(results_1['schemas']), 1)
        self.assertEqual(len(results_1['project_schemas']), 1)

        results_retrieve = retrieve(project=project)
        self.assertNotEqual(results_4, results_retrieve,
                            'only returns the affected ids NEVER ALL OF THEM')

    def test__upsert_project_artefacts__mappings(self):
        project = Project.objects.create(name='Project')
        mapping_id = str(uuid.uuid4())

        results_1 = generate(project_id=project.pk, project_name=project.name, mappings=[
            {'id': mapping_id, 'name': 'Mapping'},
        ])
        results_retrieve = retrieve(project=project)
        self.assertEqual(results_1, results_retrieve)

        self.assertEqual(results_1['project'], str(project.pk))
        self.assertEqual(results_1['schemas'], set())
        self.assertEqual(results_1['project_schemas'], set())
        self.assertEqual(results_1['mappings'], set([mapping_id]))

        mapping = Mapping.objects.get(pk=mapping_id)
        self.assertEqual(mapping.name, 'Mapping')
        self.assertEqual(mapping.revision, '1')
        self.assertEqual(mapping.definition, {'mappings': []})

        results_2 = generate(project_id=project.pk, project_name=project.name, mappings=[
            # in this case nothing changes
            {'id': mapping_id, 'name': 'Mapping 2'},
        ])
        self.assertEqual(results_1, results_2)

        mapping.refresh_from_db()
        self.assertEqual(mapping.name, 'Mapping')
        self.assertEqual(mapping.revision, '1')
        self.assertEqual(mapping.definition, {'mappings': []})

        results_3 = generate(project_id=project.pk, project_name=project.name, mappings=[
            # in this case the definition is updated
            {'id': mapping_id, 'definition': {}},
        ])
        self.assertEqual(results_1, results_3)

        mapping.refresh_from_db()
        self.assertEqual(mapping.name, 'Mapping')
        self.assertEqual(mapping.revision, '1')
        self.assertEqual(mapping.definition, {})

        # creating a new empty mapping
        results_4 = generate(project_id=project.pk, project_name=project.name, mappings=[
            # It's possible to create empty mappings!!!
            {},
        ])
        self.assertNotEqual(results_1, results_4, 'only returns the affected ids')
        self.assertEqual(len(results_1['mappings']), 1)

        results_retrieve = retrieve(project=project)
        self.assertNotEqual(results_4, results_retrieve,
                            'only returns the affected ids NEVER ALL OF THEM')

    def test__upsert_project_artefacts__atomicity(self):

        new_project = Project.objects.create(name='Project')
        project_id = str(uuid.uuid4())
        self.assertNotEqual(str(new_project.pk), project_id)

        self.assertEqual(Project.objects.filter(pk=project_id).count(), 0)
        with self.assertRaises(IntegrityError) as iep:
            generate(
                project_id=project_id,
                project_name='Project',  # already in use
            )
        self.assertIsNotNone(iep)
        self.assertIn('DETAIL:  Key (name)=(Project) already exists.', str(iep.exception))
        self.assertEqual(Project.objects.filter(pk=project_id).count(), 0)

        # in the middle of the process with objects already created
        self.assertEqual(Project.objects.filter(pk=project_id).count(), 0)
        self.assertEqual(Schema.objects.all().count(), 0)
        with self.assertRaises(IntegrityError) as ies:
            generate(
                project_id=project_id,
                project_name='Project 2',  # not in use
                schemas=[
                    {'name': 'Schema'},    # this will be created
                    {'name': 'Schema'},    # but this one will complain
                ]
            )
        self.assertIsNotNone(ies)
        self.assertIn('DETAIL:  Key (name)=(Schema) already exists.', str(ies.exception))
        # all the actions are reverted
        self.assertEqual(Project.objects.filter(pk=project_id).count(), 0)
        self.assertEqual(Schema.objects.all().count(), 0)