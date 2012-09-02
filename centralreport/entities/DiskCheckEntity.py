#
# CentralReport Entity
#

import datetime

class DiskCheckEntity:
    """ This entity represent a disk check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.name = ""
        self.size = float(0)
        self.used = float(0)
        self.free = float(0)


