# -*- coding: utf-8 -*-
import json


def object_converter(data, encod):
    """
        Represent instance of a class converted in what you want.
        @param encod: Encoded format like JSON...
        @param data: An object
        @Return: String that reprent encoded object.
    """

    def serialize(data):
        """
            Serialize the object whatever is type
            @param data: An object
        """
        if isinstance(data, (bool, int, long, float, basestring)):
            return data
        elif isinstance(data, dict):
            data = data.copy()
            for key in data:
                data[key] = serialize(data[key])
            return data
        elif isinstance(data, list):
            return [serialize(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(serialize([item for item in data]))
        elif hasattr(data, '__dict__'):
            return serialize(data.__dict__)
        else:
            return str(data)  # convert to string

    # We can add "if" for all type we want
    if "json" == encod:
        return json.dumps(serialize(data))
    else:
        return serialize(data)

