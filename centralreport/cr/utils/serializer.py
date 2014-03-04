# -*- coding: utf-8 -*-

"""
    CentralReport - serializer module
        Contains functions to parse data to a serialized format

    https://github.com/CentralReport/
"""

import json

FORMAT_STRING = 'string'
FORMAT_JSON = 'json'


def serialize(data, encod=FORMAT_STRING):
    """
        Serializes the object whatever its type is

        @param data: An object
        @param encod: Encoded format (see serializer.FORMAT_xxxx variables)
        @Return: A string representing the serialized object.
    """

    if encod == FORMAT_JSON:
        return json.dumps(serialize(data))

    if isinstance(data, (bool, int, long, float, basestring)):
        return data

    if isinstance(data, dict):
        data = data.copy()
        for key in data:
            data[key] = serialize(data[key])
        return data

    if isinstance(data, list):
        return [serialize(item) for item in data]

    if isinstance(data, tuple):
        return tuple(serialize([item for item in data]))

    if hasattr(data, '__dict__'):
        return serialize(data.__dict__)

    return str(data)

