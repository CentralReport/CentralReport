#
# CentralReport Entity
#

import datetime,json

class DiskCheckEntity:
    """ This entity represent a disk check for the current host. """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.name = ""
        self.size = float(0)
        self.used = float(0)
        self.free = float(0)


    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """
        return json.dumps({'date' : self.date.strftime('%s'),
                           'name' : self.name,
                           'size' : self.size,
                           'used' : self.used,
                           'free' : self.free})
