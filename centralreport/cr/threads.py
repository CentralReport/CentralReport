# -*- coding: utf-8 -*-

"""
    CentralReport - Threads module
        Contains threads used by CentralReport to perform periodic actions

    https://github.com/CentralReport
"""

from datetime import datetime
import threading
import time

from cr import collectors
from cr import data
from cr import log
from cr.entities import checks
import cr.host
from cr.tools import Config


class Checks(threading.Thread):
    """
        Thread performing periodically checks.
    """

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
        log.log_debug('ThreadChecks is starting...')  # Standard output


        if cr.host.get_current_host().os == cr.host.OS_MAC:
            self.MyCollector = collectors.MacCollector()
        elif cr.host.get_current_host().family == cr.host.FAMILY_LINUX:
            self.MyCollector = collectors.DebianCollector()
        else:
            raise TypeError

        # Perform a check every xx ticks (1 tick = 1 second)
        try:
            self.tickPerformCheck = int(Config.get_config_value('Checks', 'interval'))
        except:
            self.tickPerformCheck = 60

        log.log_debug('Interval between two checks: %s seconds' % self.tickPerformCheck)

        self.start()

    def run(self):
        """
            Manages the execution of new checks periodically.
        """

        while Checks.performChecks:
            if self.tickPerformCheck <= self.tickCount:
                try:
                    self.perform_check()
                except Exception as e:
                    log.log_error('Error performing a new check: %s' % e)

                log.log_debug('Next checks in %s seconds...' % self.tickPerformCheck)
                self.tickCount = 0

            self.tickCount += 1
            time.sleep(1)

    def perform_check(self):
        """
            Performs a new global check.
            Can be raise a error if a check fail.
        """

        log.log_debug('---- New check -----')
        check_entity = checks.Check()

        # Checking CPU
        log.log_debug('Performing a CPU check...')
        check_entity.cpu = self.MyCollector.get_cpu()

        # Checking memory
        log.log_debug('Performing a memory check...')
        check_entity.memory = self.MyCollector.get_memory()

        # Checking Load Average
        log.log_debug('Performing a load average check...')
        check_entity.load = self.MyCollector.get_loadaverage()

        # Checking disks information
        log.log_debug('Performing a disk check....')
        check_entity.disks = self.MyCollector.get_disks()

        # Updating last check date...
        check_entity.date = datetime.now()

        data.last_check = check_entity

        log.log_debug('All checks are done')
