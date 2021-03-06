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

from . import CouchDBTestCase
from .. import api as couchdb
from .. import utils


class UtilsTests(CouchDBTestCase):

    def test_force_put_doc(self):
        path = self.test_db + '/foo'

        utils.force_put_doc(path, {'_id': 'foo', 'new': True})
        r = couchdb.get(path)
        r.raise_for_status()
        self.assertTrue(r.json()['new'])

        utils.force_put_doc(path, {'_id': 'foo', 'new': False})
        r = couchdb.get(path)
        r.raise_for_status()
        self.assertFalse(r.json()['new'])

    def test_fetch_db_docs(self):
        # clean db
        d1 = utils.fetch_db_docs(self.test_db, 0)
        # Note: in CouchDB 1.x the `last_seq` values are integers,
        # but since CouchDB 2.x they turned into strings like `0-zzzzzzz`
        self.assertEqual(str(d1['last_seq'])[0], '0', msg='last seq starts in 0')
        self.assertEqual(len(d1['docs']), 0, msg='empty db')

        # two new docs
        foo = couchdb.post(self.test_db, json={'_id': 'foo'}).json()
        couchdb.post(self.test_db, json={'_id': 'bar'})
        d2 = utils.fetch_db_docs(self.test_db, d1['last_seq'])
        self.assertNotEqual(d2['last_seq'], d1['last_seq'], msg='last seq changed')
        self.assertEqual(len(d2['docs']), 2, msg='changed or new docs')

        # one doc changed since last check
        couchdb.post(self.test_db, json={'_id': foo['id'], '_rev': foo['rev']})
        d3 = utils.fetch_db_docs(self.test_db, d2['last_seq'])
        self.assertNotEqual(d3['last_seq'], d2['last_seq'], msg='last seq changed')
        self.assertEqual(len(d3['docs']), 1, msg='1 doc changes since last seq')
        self.assertEqual(d3['docs'][0]['_id'], foo['id'])

        # no changes since last check
        d4 = utils.fetch_db_docs(self.test_db, d3['last_seq'])
        self.assertEqual(d4['last_seq'], d3['last_seq'], msg='last seq not changed')
        self.assertEqual(len(d4['docs']), 0, msg='No docs changed since last seq')
