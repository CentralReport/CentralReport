# -*- coding: utf-8 -*-

"""
    CentralReport - Host module
        Contains all entities about current host (infos and disks)

    https://github.com/CentralReport
"""

import datetime


class Host:
    """
        Entity containing details about actual host.
    """

    def __init__(self):
        self.architecture = ''

        self.family = ''
        self.variant = ''
        self.os = ''

        # TODO: move it in CPU check.

        self.cpu_model = ''
        self.cpu_count = 1

        self.date = datetime.datetime.now()
        self.hostname = ''

        # Unix/Linux attributes

        self.kernel_name = ''
        self.kernel_version = ''

        # OS informations

        self.os_name = ''
        self.os_version = ''

        self.language = 'Python'  # CentralReport app language
        self.model = ''  # Only for Mac OS

        self.uuid = ''
        self.key = ''
