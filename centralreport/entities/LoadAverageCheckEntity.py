#
# CentralReport Entity
#

import datetime,json

class LoadAverageCheckEntity:
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
        return json.dumps({'date' : self.date.strftime('%s'),
                           'last1m' : self.last1m,
                           'last5m' : self.last5m,
                           'last15m' : self.last15m})
