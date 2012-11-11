#
# CentralReport - Indev version
#

# This module contains all entities about the current host :
# infos (caracteristics)
# disks

import datetime,json


class Infos:
    """ This entity contain some datas about actual host """

    def __init__(self):
        self.date = datetime.datetime.now()

        self.os = ""
        self.hostname = ""
        self.architecture = ""

        # TODO : move it in CPU check.
        self.cpuModel = ""
        self.cpuCount = 1

        # Unix/Linux attributes
        self.kernelName = ""
        self.kernelVersion = ""

        # Unique uuid
        self.uuid = ""

        # Only for Mac OS
        self.model = ""

        # CentralReport app language
        self.language = 'Python'



    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """
        return json.dumps({'type' : 'host',
                           'uuid' : self.uuid,
                           'date' : self.date.strftime('%s'),
                           'os' : self.os,
                           'hostname' : self.hostname,
                           'architecture' : self.architecture,
                           'cpuModel' : self.cpuModel,
                           'kernel_name' : self.kernelName,
                           'kernel_version' : self.kernelVersion,
                           'model' : self.model,
                           'language' : self.language})





class Disks:
    """ This entity contain checks for all disks """

    def __init__(self):
        self.date = datetime.datetime.now()
        self.checks = list()


    def jsonSerialize(self):
        """
            Serialize this entity in JSON
        """
        return json.dumps({'date' : self.date.strftime('%s'),
                           'disks' : self.checks})