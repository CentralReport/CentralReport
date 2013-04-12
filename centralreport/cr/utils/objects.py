# -*- coding: utf-8 -*-

"""
    CentralReport - serializer module
        Contains functions to parse data to a serialized format

    https://github.com/CentralReport/
"""

import json


def object_converter(data, encod):
    """
        Represents a data converted into a given serialized format.
        @param data: An object
        @param encod: Encoded format like JSON...
        @Return: A string representing the serialized object.
    """

    def serialize(data):
        """
            Serializes the object whatever its type is
            @param data: An object
            @Return: A string representing the serialized object.
        """
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

        return str(data)  # converts to string

    # We can add "if" for all type we want
    if "json" == encod:
        return json.dumps(serialize(data))

    return serialize(data)

