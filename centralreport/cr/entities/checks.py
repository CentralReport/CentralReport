# -*- coding: utf-8 -*-

"""
    CentralReport - Checks module
        Contains all check entities

    https://github.com/miniche/CentralReport/
"""

import datetime
from cr.utils import object


class Check:
    """
        Entity representing a complete check
    """

    def __init__(self):
        self.date = datetime.datetime.now()

        self.cpu = None
        self.disks = None
        self.memory = None
        self.load = None

    def serialize(self):
        """
            Serializes this entity in JSON
        """

        object.object_converter(self, "json")


class Cpu:
    """
        Entity representing a cpu check for the current host.
    """

    def __init__(self):
        self.idle = float(0)
        self.system = float(0)
        self.user = float(0)

    def serialize(self):
        """
            Serializes this entity in JSON
        """

        object.object_converter(self, "json")


class Disks:
    """
        Entity containing checks for all the disks.
    """

    def __init__(self):
        self.disks = list()

    def serialize(self):
        """
            Serializes this entity in JSON.
        """

        all_disks = []

        for disk in self.disks:
            check_disk = {
                'name': disk.name,
                'free': disk.free,
                'total': disk.size
            }
            all_disks.append(check_disk)

        object.object_converter(all_disks, "json")


class Disk:
    """
        Entity representing a disk check for the current host.
    """

    def __init__(self):
        self.free = float(0)
        self.name = ''
        self.size = float(0)
        self.unix_name = ''
        self.used = float(0)

    def serialize(self):
        """
            Serializes this entity in JSON
        """

        object.object_converter(self, "json")


class LoadAverage:
    """
        Entity representing a load average check for the current host.
    """

    def __init__(self):
        self.last1m = float(0)
        self.last5m = float(0)
        self.last15m = float(0)
        self.uptime = int(0)  # Uptime in seconds

    def serialize(self):
        """
            Serializes this entity in JSON
        """

        object.object_converter(self, "json")


class Memory:
    """
        Entity representing a memory check for the current host.
    """

    def __init__(self):
        self.active = float(0)
        self.free = float(0)
        self.inactive = float(0)
        self.resident = float(0)
        self.swap_free = float(0)
        self.swap_size = float(0)
        self.swap_used = float(0)
        self.total = float(0)

    def serialize(self):
        """
            Serializes this entity in JSON
        """

        object.object_converter(self, "json")
