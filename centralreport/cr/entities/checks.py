# -*- coding: utf-8 -*-

"""
    CentralReport - Checks module
        Contains all check entities

    https://github.com/CentralReport
"""

import datetime


class Check:
    """
        Entity representing a complete check
    """

    def __init__(self):
        self.date = datetime.datetime.now()

        #: @type cpu: cr.entities.checks.Cpu
        self.cpu = None

        #: @type disks: cr.entities.checks.Disks
        self.disks = None

        #: @type memory: cr.entities.checks.Memory
        self.memory = None

        #: @type load: cr.entities.checks.LoadAverage
        self.load = None


class Cpu:
    """
        Entity representing a cpu check for the current host.
    """

    def __init__(self):
        self.idle = float(0)
        self.system = float(0)
        self.user = float(0)


class Disks:
    """
        Entity containing checks for all the disks.
    """

    def __init__(self):

        #: @type disks: list of cr.entities.checks.Disk
        self.disks = list()


class Disk:
    """
        Entity representing a disk check for the current host.
    """

    def __init__(self):
        self.name = ''
        self.display_name = ''
        self.uuid = ''
        self.size = float(0)
        self.free = float(0)
        self.used = float(0)


class LoadAverage:
    """
        Entity representing a load average check for the current host.
    """

    def __init__(self):
        self.last1m = float(0)
        self.last5m = float(0)
        self.last15m = float(0)
        self.uptime = int(0)  # Uptime in seconds


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
