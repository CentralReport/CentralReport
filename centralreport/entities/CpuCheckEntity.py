#
# CentralReport Entity
#

import datetime

class CpuCheckEntity:
    """ This entity represent a cpu check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.idle = float(0)
        self.user = float(0)
        self.system = float(0)


