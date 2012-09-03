#
# CentralReport Entity
#

import datetime

class HostEntity:
    """ This entity contain some datas about actual host """

    def __init__(self):
        self.date = datetime.datetime.now()

        self.os = ""
        self.hostname = ""
        self.architecture = ""

        self.cpuModel = ""
        self.cpuCount = 0

        # Unix/Linux attributes
        self.kernelName = ""
        self.kernelVersion = ""

        # Unique uuid
        self.uuid = ""

        # Only for Mac OS
        self.model = ""

        # CentralReport app language
        self.language = 'Python'


