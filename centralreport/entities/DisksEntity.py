#
# CentralReport Entity
#

import datetime

class DisksEntity:
    """ This entity contain checks for all actual disks """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.checks = list()

