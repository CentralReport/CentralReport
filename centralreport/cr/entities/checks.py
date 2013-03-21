# -*- coding: utf-8 -*-

"""
    CentralReport - Checks module
        Contains all check entities

    https://github.com/miniche/CentralReport/
"""


class Cpu:

    """
        Entity representing a cpu check for the current host.
    """

    def __init__(self):
        self.idle = float(0)
        self.system = float(0)
        self.user = float(0)

    def json_serialize(self):
        """
            Serializes this entity in JSON
        """

        return {
            'idle': self.idle,
            'system': self.system,
            'user': self.user
        }


class Disks:
    """
        Entity containing checks for all the disks.
    """

    def __init__(self):
        self.disks = list()

    def json_serialize(self):
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

        return all_disks


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

    def json_serialize(self):
        """
            Serializes this entity in JSON
        """

        return {
            'free': self.free,
            'name': self.name,
            'size': self.size,
            'unix_name': self.unix_name,
            'used': self.used
        }


class LoadAverage:

    """
        Entity representing a load average check for the current host.
    """

    def __init__(self):
        self.last1m = float(0)
        self.last5m = float(0)
        self.last15m = float(0)
        self.uptime = int(0)  # Uptime in seconds

    def json_serialize(self):
        """
            Serializes this entity in JSON
        """

        return {
            'last1m': self.last1m,
            'last5m': self.last5m,
            'last15m': self.last15m,
            'uptime': self.uptime
        }


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

    def json_serialize(self):
        """
            Serializes this entity in JSON
        """

        return {
            'active': self.active,
            'free': self.free,
            'inactive': self.inactive,
            'resident': self.resident,
            'swap_free': self.swap_free,
            'swap_size': self.swap_size,
            'swap_used': self.swap_used,
            'total': self.total
        }
