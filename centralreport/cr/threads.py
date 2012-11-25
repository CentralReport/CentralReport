#
# CentralReport - Indev version
#

import threading
import time
import datetime
import cr.collectors as crCollectors
import cr.log as crLog
from cr.tools import Config


class Checks(threading.Thread):
    """
        This thread will perform periodically checks.
    """

    # True = perform checks...
    performChecks = True

    # Initial Count (Perform a check when starting)
    tickCount = 60
    # Perform a check every xx ticks (1 tick = 1 second)
    tickPerformCheck = 60

    # Get host informations
    hostEntity = None

    # Last checks (with new entities classes)
    last_check_date = None
    last_check_cpu = None
    last_check_memory = None
    last_check_loadAverage = None
    last_check_disk = None

    def __init__(self):
        threading.Thread.__init__(self)

        # Standard output
        crLog.writeDebug('ThreadChecks is starting...')

        # What is the current os ?
        if Config.HOST_CURRENT == Config.HOST_MAC:
            self.MyCollector = crCollectors.MacCollector()
        elif(Config.HOST_CURRENT == Config.HOST_DEBIAN) \
            | (Config.HOST_CURRENT == Config.HOST_UBUNTU):
            self.MyCollector = crCollectors.DebianCollector()

        self.start()

    def run(self):
        """
            Execute checks
        """

        # Getting informations about the current host
        Checks.hostEntity = self.MyCollector.get_infos()

        while Checks.performChecks:

            if self.tickCount == self.tickPerformCheck:
                crLog.writeDebug('---- New check -----')

                # Checking CPU
                if Config.config_enable_check_cpu:
                    crLog.writeDebug('Do a CPU check...')
                    Checks.last_check_cpu = self.MyCollector.get_cpu()

                # Checking memory
                if Config.config_enable_check_memory:
                    crLog.writeDebug('Do a memory check...')
                    Checks.last_check_memory = self.MyCollector.get_memory()

                # Checking Load Average
                if Config.config_enable_check_loadaverage:
                    crLog.writeDebug('Do a load average check...')
                    Checks.last_check_loadAverage = self.MyCollector.get_loadaverage()

                # Checking disks informations
                crLog.writeDebug('Do a disk check....')
                Checks.last_check_disk = self.MyCollector.get_disks()
                Checks.last_check_date = datetime.datetime.now()  # Update the last check date

                # Wait 60 seconds before next checks...
                crLog.writeDebug('All checks are done')
                crLog.writeDebug('Next checks in '+ str(self.tickPerformCheck) +' seconds...')

                self.tickCount = 0

            # new tick
            self.tickCount += 1
            time.sleep(1)

