#
# CentralReport - Indev version
#

import datetime
import json


class Cpu:
    """ This entity represent a cpu check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.idle = float(0)
        self.user = float(0)
        self.system = float(0)

    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """

        return json.dumps({
            'date': self.date.strftime('%s'),
            'idle': self.idle,
            'user': self.user,
            'system': self.system
        })


class Disk:
    """ This entity represent a disk check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.name = ''
        self.size = float(0)
        self.used = float(0)
        self.free = float(0)

    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """

        return json.dumps({
            'date': self.date.strftime('%s'),
            'name': self.name,
            'size': self.size,
            'used': self.used,
            'free': self.free
        })


class LoadAverage:
    """ This entity represent a load average check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.last1m = float(0)
        self.last5m = float(0)
        self.last15m = float(0)

    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """

        return json.dumps({
            'date': self.date.strftime('%s'),
            'last1m': self.last1m,
            'last5m': self.last5m,
            'last15m': self.last15m
        })


class Memory:
    """ This entity represent a memory check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.total = float(0)
        self.free = float(0)
        self.active = float(0)
        self.inactive = float(0)
        self.resident = float(0)

        self.swapSize = float(0)
        self.swapUsed = float(0)
        self.swapFree = float(0)

    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """

        return json.dumps({
            'date': self.date.strftime('%s'),
            'total': self.total,
            'free': self.free,
            'active': self.active,
            'inactive': self.inactive,
            'resident': self.resident,
            'swap_size': self.swapSize,
            'swap_used': self.swapUsed
        })
