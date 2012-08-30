#
# CentralReport Entity
#

import datetime

class MemoryCheckEntity:
    """ This entity represent a memory check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.total = float(0)
        self.free = float(0)
        self.active = float(0)
        self.inactive = float(0)
        self.resident = float(0)

        self.swapTotal = float(0)
        self.swapUsed = float(0)


