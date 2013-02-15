# -*- coding: utf-8 -*-

"""
    CentralReport - Threads module
        Contains threads used by CentralReport to perform periodic actions

    https://github.com/miniche/CentralReport/
"""

import datetime
import threading
import time

import cr.collectors as crCollectors
import cr.log as crLog
import cr.utils.text as crUtilsText
from cr.tools import Config


class Checks(threading.Thread):
    """
        Thread performing periodically checks.
    """

    hostEntity = None  # Get host informations

    # Last checks (with new entities classes)

    last_check_cpu = None
    last_check_date = None
    last_check_disk = None
    last_check_loadAverage = None
    last_check_memory = None

    performChecks = True  # True = perform checks...
    tickCount = 60  # Initial Count (Perform a check when starting)

    def __init__(self):
        threading.Thread.__init__(self)
        crLog.writeDebug('ThreadChecks is starting...')  # Standard output

        # What is the current os?

        if Config.HOST_CURRENT == Config.HOST_MAC:
            self.MyCollector = crCollectors.MacCollector()
        elif (Config.HOST_CURRENT == Config.HOST_DEBIAN) | (Config.HOST_CURRENT == Config.HOST_UBUNTU):
            self.MyCollector = crCollectors.DebianCollector()

        # Perform a check every xx ticks (1 tick = 1 second)

        try:
            self.tickPerformCheck = int(Config.getConfigValue('Checks', 'interval'))
        except:
            self.tickPerformCheck = 60

        crLog.writeDebug('Interval between two checks: %s seconds' % self.tickPerformCheck)

        self.start()

    def run(self):
        """
            Executes checks.
        """

        # Getting informations about the current host

        Checks.hostEntity = self.MyCollector.get_infos()

        while Checks.performChecks:
            if self.tickPerformCheck <= self.tickCount:
                crLog.writeDebug('---- New check -----')

                # Checking CPU
                if crUtilsText.textToBool(Config.getConfigValue('Checks', 'enable_cpu_check')):
                    crLog.writeDebug('Doing a CPU check...')
                    Checks.last_check_cpu = self.MyCollector.get_cpu()

                # Checking memory
                if crUtilsText.textToBool(Config.getConfigValue('Checks', 'enable_memory_check')):
                    crLog.writeDebug('Doing a memory check...')
                    Checks.last_check_memory = self.MyCollector.get_memory()

                # Checking Load Average
                if crUtilsText.textToBool(Config.getConfigValue('Checks', 'enable_load_check')):
                    crLog.writeDebug('Doing a load average check...')
                    Checks.last_check_loadAverage = self.MyCollector.get_loadaverage()

                # Checking disks informations
                if crUtilsText.textToBool(Config.getConfigValue('Checks', 'enable_disks_check')):
                    crLog.writeDebug('Doing a disk check....')
                    Checks.last_check_disk = self.MyCollector.get_disks()

                # Updating last check date...

                Checks.last_check_date = datetime.datetime.now()  # Update the last check date

                # Wait 60 seconds before next checks...

                crLog.writeDebug('All checks are done')
                crLog.writeDebug('Next checks in %s seconds...' % self.tickPerformCheck)

                self.tickCount = 0

            # new tick

            self.tickCount += 1
            time.sleep(1)
