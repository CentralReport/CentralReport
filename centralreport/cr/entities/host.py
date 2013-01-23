#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# CentralReport - Indev version
#

# This module contains all entities about the current host:
# infos (caracteristics)
# disks

import datetime
import json


class Infos:

    """
        Entity containing datas about actual host.
    """

    def __init__(self):
        self.architecture = ''

        # TODO : move it in CPU check.

        self.cpuModel = ''
        self.cpuCount = 1

        self.date = datetime.datetime.now()
        self.hostname = ''

        # Unix/Linux attributes

        self.kernelName = ''
        self.kernelVersion = ''

        # OS informations

        self.osName = ''
        self.osVersion = ''

        self.language = 'Python'  # CentralReport app language
        self.model = ''  # Only for Mac OS
        self.os = ''
        self.uuid = ''

    def jsonSerialize(self):
        """
            Serializes this entity in JSON.
        """

        return json.dumps({
            'architecture': self.architecture,
            'cpuCount': self.cpuCount,
            'cpuModel': self.cpuModel,
            'date': self.date.strftime('%s'),
            'hostname': self.hostname,
            'kernel_name': self.kernelName,
            'kernel_version': self.kernelVersion,
            'model': self.model,
            'language': self.language,
            'os': self.os,
            'type': 'host',
            'uuid': self.uuid,
            })


class Disks:

    """
        Entity containing checks for all the disks.
    """

    def __init__(self):
        self.checks = list()
        self.date = datetime.datetime.now()

    def jsonSerialize(self):
        """
            Serializes this entity in JSON.
        """

        return json.dumps({'date': self.date.strftime('%s'),
                          'disks': self.checks})
