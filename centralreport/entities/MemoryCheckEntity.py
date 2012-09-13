#
# CentralReport Entity
#

import datetime,json

class MemoryCheckEntity:
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
        return json.dumps({'date' : self.date.strftime('%s'),
                           'total' : self.total,
                           'free' : self.free,
                           'active' : self.active,
                           'inactive' : self.inactive,
                           'resident' : self.resident,
                           'swap_size' : self.swapSize,
                           'swap_used' : self.swapUsed})


