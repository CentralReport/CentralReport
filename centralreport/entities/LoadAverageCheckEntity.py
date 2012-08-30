#
# CentralReport Entity
#

import datetime

class LoadAverageCheckEntity:
    """ This entity represent a load average check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.last1m = float(0)
        self.last5m = float(0)
        self.last15m = float(0)


