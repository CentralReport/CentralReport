#
# CentralReport Entity
#

import datetime,json

class CpuCheckEntity:
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
        return json.dumps({'date' : self.date.strftime('%s'),
                           'idle' : self.idle,
                           'user' : self.user,
                           'system' : self.system})


