# -*- coding: utf-8 -*-

"""
    CentralReport - Webservices module
        Contains all entities used with webservices.

    https://github.com/miniche/CentralReport/
"""

import json


class Full:
    """
        This entity contains all infos of the host
    """

    def __init__(self):
        self.checks = list()
        self.host = None

    def json_serialize(self):
        """
            Serializes this entity in JSON.
        """

        host_data = {
            'host': self.host.serialize()
        }

        host_data['host']['checks'] = []

        for check in self.checks:
            host_data['host']['checks'].append(check.serialize())

        return json.dumps(host_data)


class GetStatus:
    """
        Entity used to get the host status on the remote server
    """

    def __init__(self):
        self.uuid = ""
        self.key = ""
        self.hostname = ""
        self.os = ""
        self.os_version = ""

    def serialize(self):
        """
            Serialize the current object
            @return: a dict with all values
        """

        return {
            'uuid': self.uuid,
            'key': self.key,
            'hostame': self.hostname,
            'os': self.os,
            'os_version': self.os_version
        }


class WebServiceReturn:
    """
        This entity contains the result of a webservice
    """

    def __init__(self):
        self.code = 0
        self.headers = []
        self.text = ""

