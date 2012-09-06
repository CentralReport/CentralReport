#
# CentralReport Entity
#

import datetime,json

class DisksEntity:
    """ This entity contain checks for all actual disks """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.checks = list()


    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """
        return json.dumps({'date' : self.date.strftime('%s'),
                           'disks' : self.checks})
