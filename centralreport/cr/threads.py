# -*- coding: utf-8 -*-

"""
    CentralReport - Threads module
        Contains threads used by CentralReport to perform periodic actions

    https://github.com/miniche/CentralReport/
"""

from datetime import datetime
import threading
import time

from cr import collectors
from cr import log
from cr.entities import checks
from cr.tools import Config


class Checks(threading.Thread):
    """
        Thread performing periodically checks.
    """

    # Host related information (entities.host.Infos())
    host_infos = None

    # Last checks (entities.checks.Check())
    last_check = None

    performChecks = True  # True = perform checks...
    tickCount = 60  # Initial Count (Perform a check when starting)

    def __init__(self):
        threading.Thread.__init__(self)
        log.log_debug('ThreadChecks is starting...')  # Standard output

        # What is the current os?

        if Config.HOST_CURRENT == Config.HOST_MAC:
            self.MyCollector = collectors.MacCollector()
        elif (Config.HOST_CURRENT == Config.HOST_DEBIAN) or (Config.HOST_CURRENT == Config.HOST_UBUNTU):
            self.MyCollector = collectors.DebianCollector()

        # Perform a check every xx ticks (1 tick = 1 second)

        try:
            self.tickPerformCheck = int(Config.get_config_value('Checks', 'interval'))
        except:
            self.tickPerformCheck = 60

        log.log_debug('Interval between two checks: %s seconds' % self.tickPerformCheck)

        self.start()

    def run(self):
        """
            Executes checks.
        """

        # Getting information about the current host

        Checks.host_infos = self.MyCollector.get_infos()

        while Checks.performChecks:
            if self.tickPerformCheck <= self.tickCount:
                log.log_debug('---- New check -----')
                check_entity = checks.Check()

                # Checking CPU
                log.log_debug('Doing a CPU check...')
                check_entity.cpu = self.MyCollector.get_cpu()

                # Checking memory
                log.log_debug('Doing a memory check...')
                check_entity.memory = self.MyCollector.get_memory()

                # Checking Load Average
                log.log_debug('Doing a load average check...')
                check_entity.load = self.MyCollector.get_loadaverage()

                # Checking disks information
                log.log_debug('Doing a disk check....')
                check_entity.disks = self.MyCollector.get_disks()

                # Updating last check date...
                check_entity.date = datetime.now()

                Checks.last_check = check_entity
                Remote.add_check(check_entity)

                # Wait 60 seconds before next checks...
                log.log_debug('All checks are done')
                log.log_debug('Next checks in %s seconds...' % self.tickPerformCheck)

                self.tickCount = 0

            # new tick

            self.tickCount += 1
            time.sleep(1)


class Remote(threading.Thread):
    """
        This class is used for sending Checks to the remote server
    """

    checks = list()  # Checks that need to be sent to the remote server

    is_enable = False  # "True" only if this daemon is able to send checks to the remote server

    _perform_send = True

    def __init__(self):
        threading.Thread.__init__(self)

        log.log_debug('SendCheck thread is starting...')
        self.start()

    def run(self):
        """
            Sends data to remote server
        """

        while Checks.host_infos is None:
            log.log_debug('SendCheck: Waiting for the first check...')
            time.sleep(4)

        while Remote._perform_send:

            if Checks.host_infos.key == '':
                log.log_debug('SendCheck: Remote key undefined!')
            else:
                # TODO: Connection with the remote server with HATEOAS and REST APIs
                pass

            time.sleep(60)


    @staticmethod
    def add_check(check):
        """
            Adds that will be sent to the remote server as soon as possible.
            The check is not added if CR is unable to communicate with the remote server.

            @param check: The check entity
            @type check: cr.entities.checks.Check
        """
        if Remote.is_enable:
            log.log_debug('This check will be sent to the remote server ASAP.')
            Remote.checks.append(check)
        else:
            log.log_debug('Check ignored: Remote server is disable.')
