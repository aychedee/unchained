# Copyright © 2014 Hansel Dunlop (coding: utf8)
# All rights reserved

import pickle
from collections import MutableMapping
from unittest import TestCase
from django.utils import six

if six.PY3:
    unicode = str

from unchained import fields


class JSONTest(TestCase):

    def test_has_a_json_string_attr_containing_original_string(self):
        jd = fields.JSON('{"hello": "world"}')

        self.assertEqual(jd.json_string, '{"hello": "world"}')

    def test_falls_back_to_string_type_when_given_an_invalid_object(self):
        result = fields.JSON('{hello": "world"}')

        self.assertEqual(result, '{hello": "world"}')

    def test_lookups_work(self):
        jd = fields.JSON('{"hello": "world"}')

        self.assertEqual(jd['hello'], 'world')

    def test_returns_a_dict_subclass_for_json_object_type(self):
        jd = fields.JSON('{"hello": "world"}')

        self.assertTrue(issubclass(jd.__class__, MutableMapping))

    def test_returns_a_string_subclass_for_json_string_types(self):
        jd = fields.JSON('"yeah alright"')

        self.assertTrue(issubclass(jd.__class__, str))

    def test_with_dict_type(self):
        result = fields.JSON({'hello': 'world'})

        self.assertEqual(result.json_string, '{"hello": "world"}')
        self.assertEqual(result['hello'], 'world')

    def test_with_list_type(self):
        result = fields.JSON([1, 2, 3, {'hello': 'world'}])

        self.assertEqual(result.json_string, '[1, 2, 3, {"hello": "world"}]')
        self.assertEqual(result[2], 3)

    def test_with_non_json_string(self):
        result = fields.JSON('hello world, this is weird')

        self.assertEqual(result.json_string, '"hello world, this is weird"')


class JsonDictTest(TestCase):

    def test_json_string_attribute_gets_updated_when_item_set(self):
        jd = fields.JSON.JsonDict(
            {'dinner': 'couscous'}, '')

        jd['dinner'] = 'cod'

        self.assertEqual(jd.json_string, '{"dinner": "cod"}')
        self.assertEqual(jd['dinner'], 'cod')

    def test_is_iterable(self):
        jd = fields.JSON.JsonDict(
            {'dinner': 'couscous', 'lunch': '3 martini'}, '')

        result = sorted([(k, jd[k]) for k in jd])

        self.assertEqual(
            result,
            [('dinner', 'couscous'), ('lunch', '3 martini')]
        )

    def test_has_length(self):
        jd = fields.JSON.JsonDict(
            {'dinner': 'couscous', 'lunch': '3 martini'}, '')

        self.assertEqual(len(jd), 2)

    def test_items_can_be_deleted(self):
        jd = fields.JSON.JsonDict(
            {'dinner': 'couscous', 'lunch': '3 martini'}, '')

        del jd['lunch']

        self.assertEqual(jd.get('lunch', None), None)
        self.assertEqual(jd.json_string, '{"dinner": "couscous"}')

    def test_compares_equal_to_dict(self):
        original_dict = {'dinner': 'couscous', 'lunch': '3 martini'}
        jd = fields.JSON.JsonDict(original_dict, '')

        self.assertEqual(jd, original_dict)

    def test_sub_dicts_are_converted_to_jsondicts(self):
        original_dict = {'dinner': 'couscous', 'lunch': '3 martini'}
        jd = fields.JSON.JsonDict(original_dict, '')
        jd['key'] = original_dict

        self.assertIsInstance(jd['key'], fields.JSON.JsonDict)

    def test_can_be_pickled_and_unpickled(self):
        original_dict = {'dinner': 'couscous', 'lunch': '3 martini'}
        jd = fields.JSON.JsonDict(original_dict, '')

        pickled = pickle.dumps(jd)

        unpickled = pickle.loads(pickled)

        self.assertEqual(jd, unpickled)


class JsonListTest(TestCase):

    def test_list_has_length(self):
        jl = fields.JSON.JsonList(['apples', 'squares', 'pears'], '')

        self.assertEqual(len(jl), 3)

    def test_jsonlist_updates_raw_when_modifying_contents(self):
        jl = fields.JSON.JsonList(['apples', 'squares', 'pears'], '')
        jl.append('cares')

        self.assertEqual(
            jl.json_string,
            '["apples", "squares", "pears", "cares"]')

        del jl[1]

        self.assertEqual(jl.json_string, '["apples", "pears", "cares"]')

        jl[1] = 'dears'

        self.assertEqual(jl.json_string, '["apples", "dears", "cares"]')

    def test_can_be_pickled_and_unpickled(self):
        jl = fields.JSON.JsonList(['apples', 'squares', 'pears'], '')
        pickled = pickle.dumps(jl)

        unpickled = pickle.loads(pickled)

        self.assertEqual(jl, unpickled)

    def test_compare_equal_to_primitive_lists(self):
        original_list = ['apples', 'squares', 'pears']
        jl = fields.JSON.JsonList(original_list, '')

        self.assertEqual(jl, original_list)


class JSONFieldTest(TestCase):

    def test_db_type_is_json_for_postgres_database(self):
        jf = fields.JSONField()
        connection = type('', (), {'settings_dict': dict(
            ENGINE='django.db.backends.postgresql_psycopg2')})

        field_type = jf.db_type(connection)

        self.assertEqual(field_type, 'json')

    def test_db_type_is_text_for_sqlite_database(self):
        jf = fields.JSONField()
        connection = type('', (), {'settings_dict': dict(
            ENGINE='django.db.backends.sqlite3')})

        field_type = jf.db_type(connection)

        self.assertEqual(field_type, 'text')

    def test_to_python_returns_jsonstring_instance_from_string(self):
        jf = fields.JSONField()

        py_object = jf.to_python('"hello"')

        self.assertEqual(py_object.json_string, '"hello"')
        self.assertEqual(unicode(py_object), '"hello"')

    def test_to_python_returns_jsondict_instance_from_json_string_object(self):
        jf = fields.JSONField()
        json_string = '{"hello": "hauraki"}'

        py_object = jf.to_python(json_string)

        self.assertEqual(py_object.json_string, json_string)
        self.assertEqual(py_object['hello'], 'hauraki')

    def test_to_python_returns_jsonlist_instance_from_json_list_object(self):
        jf = fields.JSONField()
        json_string = '["hello", "hauraki"]'

        py_object = jf.to_python(json_string)

        self.assertEqual(py_object.json_string, json_string)
        self.assertEqual(py_object[1], 'hauraki')

    def test_to_python_handles_none_as_type(self):
        jf = fields.JSONField()

        py_object = jf.to_python(None)

        self.assertEqual(py_object, None)

    def test_get_prep_value_with_none_type(self):
        jf = fields.JSONField()

        prep_value = jf.get_prep_value(None)

        self.assertEqual(prep_value, None)

    def test_get_prep_value_with_json_string_type(self):
        jf = fields.JSONField()

        prep_value = jf.get_prep_value(fields.JSON('"Get Prep!"'))

        self.assertEqual(prep_value, '"Get Prep!"')

    def test_get_prep_value_with_json_object_type(self):
        jf = fields.JSONField()
        raw = '{"Get": "Prep!"}'

        prep_value = jf.get_prep_value(fields.JSON(raw))

        self.assertEqual(prep_value, raw)
