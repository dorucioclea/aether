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

import json
from unittest import mock
import requests

from django.test import TestCase, override_settings
from django_eha_sdk.unittest import MockResponse

from ..kernel_utils import (
    get_kernel_auth_header,
    get_kernel_url,
    propagate_kernel_project,
    propagate_kernel_artefacts,
    KernelPropagationError,
    __upsert_kernel_artefacts as upsert_kernel,
)
from ..models import Project, Schema


@override_settings(MULTITENANCY=False)
class KernelUtilsTest(TestCase):

    def setUp(self):
        super(KernelUtilsTest, self).setUp()

        self.kernel_url = get_kernel_url()

        # create project entry
        self.project = Project.objects.create(name='sample')

        # create schemas entries
        self.schema_1 = Schema.objects.create(
            name='no-id',
            project=self.project,
            avro_schema={
                'name': 'NoId',
                'type': 'record',
                'fields': [],
            },
        )
        self.schema_2 = Schema.objects.create(
            name='id',
            project=self.project,
            avro_schema={
                'namespace': 'my.name.space',
                'name': 'Id',
                'type': 'record',
                'fields': [{'name': 'id', 'type': 'string'}],
            },
        )

        self.KERNEL_ID_1 = str(self.schema_1.kernel_id)
        self.KERNEL_ID_2 = str(self.schema_2.kernel_id)

        self.KERNEL_HEADERS = get_kernel_auth_header()
        self.PROJECT_URL = f'{self.kernel_url}/projects/{str(self.project.project_id)}/'

        self.MAPPING_URL_1 = f'{self.kernel_url}/mappings/{self.KERNEL_ID_1}/'
        self.SCHEMA_URL_1 = f'{self.kernel_url}/schemas/{self.KERNEL_ID_1}/'

        self.MAPPING_URL_2 = f'{self.kernel_url}/mappings/{self.KERNEL_ID_2}/'
        self.SCHEMA_URL_2 = f'{self.kernel_url}/schemas/{self.KERNEL_ID_2}/'

        # check that nothing exists already in kernel
        response = requests.get(self.PROJECT_URL, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 404)

        response = requests.get(self.MAPPING_URL_1, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 404)
        response = requests.get(self.SCHEMA_URL_1, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 404)

        response = requests.get(self.MAPPING_URL_2, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 404)
        response = requests.get(self.SCHEMA_URL_2, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        super(KernelUtilsTest, self).tearDown()

        # delete the test objects created in kernel testing server
        requests.delete(self.PROJECT_URL, headers=self.KERNEL_HEADERS)
        requests.delete(self.SCHEMA_URL_1, headers=self.KERNEL_HEADERS)
        requests.delete(self.SCHEMA_URL_2, headers=self.KERNEL_HEADERS)

    @mock.patch('aether.sync.api.kernel_utils.request', return_value=MockResponse(status_code=400))
    @mock.patch('aether.sync.api.kernel_utils.get_kernel_auth_header', return_value=None)
    def test__upsert_kernel_artefacts__no_connection(self, mock_auth, mock_patch):
        with self.assertRaises(KernelPropagationError) as kpe:
            upsert_kernel(
                project=self.project,
                artefacts={'avro_schemas': []},
            )

        self.assertIsNotNone(kpe)
        self.assertIn('Connection with Aether Kernel server is not possible.',
                      str(kpe.exception), kpe)
        mock_auth.assert_called_once()
        mock_patch.assert_not_called()

    @mock.patch('aether.sync.api.kernel_utils.request',
                return_value=MockResponse(status_code=400))
    @mock.patch('aether.sync.api.kernel_utils.get_kernel_auth_header',
                return_value={'Authorization': 'Token ABCDEFGH'})
    def test__upsert_kernel_artefacts__unexpected_error(self, mock_auth, mock_patch):
        with self.assertRaises(KernelPropagationError) as kpe:
            upsert_kernel(
                project=self.project,
                artefacts={'avro_schemas': []},
            )

        self.assertIsNotNone(kpe)
        self.assertIn('Unexpected response from Aether Kernel server',
                      str(kpe.exception), kpe)
        self.assertIn('while trying to create/update the project artefacts',
                      str(kpe.exception), kpe)
        self.assertIn(f'"{str(self.project.project_id)}"', str(kpe.exception), kpe)
        mock_auth.assert_called_once()
        mock_patch.assert_called_once_with(
            method='patch',
            url=f'{self.kernel_url}/projects/{str(self.project.project_id)}/avro-schemas/',
            json={'avro_schemas': []},
            headers={'Authorization': 'Token ABCDEFGH'},
        )

    @mock.patch('aether.sync.api.kernel_utils.request',
                return_value=MockResponse(status_code=200))
    @mock.patch('aether.sync.api.kernel_utils.get_kernel_auth_header',
                return_value={'Authorization': 'Token ABCDEFGH'})
    def test__upsert_kernel_artefacts__ok(self, mock_auth, mock_patch):
        self.assertTrue(upsert_kernel(
            project=self.project,
            artefacts={'avro_schemas': []}
        ))

        mock_auth.assert_called_once()
        mock_patch.assert_called_once_with(
            method='patch',
            url=f'{self.kernel_url}/projects/{str(self.project.project_id)}/avro-schemas/',
            json={'avro_schemas': []},
            headers={'Authorization': 'Token ABCDEFGH'},
        )

    def test__propagate_kernel_project(self):
        self.assertTrue(propagate_kernel_project(self.project))

        response = requests.get(self.PROJECT_URL, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_project = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_project['id'], str(self.project.project_id))
        self.assertIn(self.project.name, kernel_project['name'])

        # creates the artefacts for the schema 1
        response = requests.get(self.MAPPING_URL_1, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_mapping_1 = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_mapping_1['id'], self.KERNEL_ID_1)
        # last rule is #!uuid
        self.assertEqual('#!uuid', kernel_mapping_1['definition']['mapping'][-1][0])

        response = requests.get(self.SCHEMA_URL_1, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_schema_1 = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_schema_1['id'], self.KERNEL_ID_1)

        # creates the artefacts for the schema 2
        response = requests.get(self.MAPPING_URL_2, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_mapping_2 = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_mapping_2['id'], self.KERNEL_ID_2)
        self.assertNotEqual('#!uuid', kernel_mapping_2['definition']['mapping'][-1][0])

        response = requests.get(self.SCHEMA_URL_2, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_schema_2 = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_schema_2['id'], self.KERNEL_ID_2)

    def test__propagate_kernel_artefacts(self):
        self.assertTrue(propagate_kernel_artefacts(self.schema_1))

        response = requests.get(self.PROJECT_URL, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_project = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_project['id'], str(self.project.project_id))
        self.assertIn(self.project.name, kernel_project['name'])

        # creates the artefacts for the schema 1
        response = requests.get(self.MAPPING_URL_1, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_mapping_1 = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_mapping_1['id'], self.KERNEL_ID_1)

        response = requests.get(self.SCHEMA_URL_1, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 200)
        kernel_schema_1 = json.loads(response.content.decode('utf-8'))
        self.assertEqual(kernel_schema_1['id'], self.KERNEL_ID_1)

        # does not create the artefacts for the schema 2
        response = requests.get(self.MAPPING_URL_2, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 404)

        response = requests.get(self.SCHEMA_URL_2, headers=self.KERNEL_HEADERS)
        self.assertEqual(response.status_code, 404)
