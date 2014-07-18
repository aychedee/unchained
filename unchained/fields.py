# Copyright 2014 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#
from __future__ import unicode_literals
from collections import MutableMapping, MutableSequence
from django.db import models
from django.utils import six
import json


class _JsonMeta(type):

    def __call__(cls, column_data):
        try:
            pyobj = json.loads(column_data)
            json_string = column_data
        except (ValueError, TypeError):
            pyobj = column_data
            json_string = json.dumps(column_data)
        if isinstance(pyobj, dict):
            return type.__call__(JSON.JsonDict, pyobj, json_string)
        if isinstance(pyobj, list):
            return type.__call__(JSON.JsonList, pyobj, json_string)
        return type.__call__(JSON.JsonString, pyobj, json_string)


def pickle_dict(*args, **kwargs):
    return JSON.JsonDict(*args, **kwargs)


def pickle_list(*args, **kwargs):
    return JSON.JsonList(*args, **kwargs)


class JSON(six.with_metaclass(_JsonMeta)):

    class Encoder(json.JSONEncoder):
        def default(self, obj):
            return obj._data

    class InvalidJSON(Exception):
        pass

    class JsonDict(MutableMapping):

        def __init__(self, pyobj, json_string):
            self._data = {}
            self._data.update(pyobj)
            self.json_string = json_string

        def __setitem__(self, k, v):
            if isinstance(v, dict):
                v = JSON.JsonDict(v, json.dumps(v))
            self._data[k] = v
            self.update_json()

        def __delitem__(self, k):
            del self._data[k]
            self.update_json()

        def __getitem__(self, k):
            return self._data[k]

        def __iter__(self):
            return iter(self._data)

        def __len__(self):
            return len(self._data)

        def update_json(self):
            self.json_string = json.dumps(self, cls=JSON.Encoder)

        def __reduce__(self):
            return pickle_dict, (self._data, self.json_string)

        def __unicode__(self):
            return six.text_type('JsonDict({})'.format(self._data))

        __str__ = __unicode__
        __repr__ = __unicode__

    class JsonString(str):

        def __new__(self, pyobj, json_string):
            self.json_string = json_string
            return str.__new__(self, pyobj)

        def __unicode__(self):
            return "{}".format(self.json_string)

        __str__ = __unicode__
        __repr__ = __unicode__

    class JsonList(MutableSequence):

        def __init__(self, pyobj, json_string):
            self.json_string = json_string
            self._contents = list(pyobj)

        def __delitem__(self, i):
            del self._contents[i]
            self.update_json()

        def __getitem__(self, i):
            return self._contents[i]

        def __len__(self):
            return len(self._contents)

        def __eq__(self, other):
            return self._contents == other

        def __setitem__(self, i, v):
            self._contents[i] = v
            self.update_json()

        def insert(self, i, v):
            self._contents.insert(i, v)
            self.update_json()

        def update_json(self):
            self.json_string = json.dumps(self._contents)

        def __reduce__(self):
            return pickle_list, (self._contents, self.json_string)

        def __unicode__(self):
            return six.text_type(json.dumps(self._contents))

        __str__ = __unicode__
        __repr__ = __unicode__


class JSONField(six.with_metaclass(models.SubfieldBase, models.TextField)):

    description = 'A JSON database field, returns a string, list or dict type'

    def db_type(self, connection):
        if connection.settings_dict[
                'ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return 'json'
        return 'text'

    def to_python(self, value):
        if hasattr(value, 'json_string') or value is None:
            return value
        return JSON(value)

    def get_prep_value(self, value):
        '''The psycopg adaptor returns Python objects,
            but we also have to handle conversion ourselves
        '''
        if isinstance(value, JSON.JsonDict):
            return json.dumps(value, cls=JSON.Encoder)
        if isinstance(value, JSON.JsonList):
            return value.json_string
        if isinstance(value, JSON.JsonString):
            return json.dumps(value)
        return value


# introspection rules to be compatible with south
try :
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^unchained\.fields\.JSONField'])
except ImportError:
    pass
