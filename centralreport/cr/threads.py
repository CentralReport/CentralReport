# -*- coding: utf-8 -*-

"""
    CentralReport - Threads module
        Contains threads used by CentralReport to perform periodic actions

    https://github.com/CentralReport
"""

import copy
from datetime import datetime
import threading
import time

from cr import collectors
from cr import data
from cr import errors
from cr import log
from cr import online
from cr.entities import checks
from cr.tools import Config

class Checks(threading.Thread):
    """
        Thread performing periodically checks.
    """

    performChecks = True  # True = perform checks...
    tickCount = 60  # Initial Count (Perform a check when starting)

    def __init__(self):
        threading.Thread.__init__(self)
        log.log_debug('ThreadChecks is starting...')  # Standard output

        # What is the current os?

        if Config.HOST_CURRENT == Config.HOST_MAC:
            self.MyCollector = collectors.MacCollector()
        elif (Config.HOST_CURRENT == Config.HOST_DEBIAN) or (Config.HOST_CURRENT == Config.HOST_UBUNTU) or \
                (Config.HOST_CURRENT == Config.HOST_CENTOS):
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
            Manages the execution of new checks periodically.
        """

        # Getting data about the current host
        data.host_info = self.MyCollector.get_infos()

        while Checks.performChecks:
            if self.tickPerformCheck <= self.tickCount:
                try:
                    self.perform_check()
                except Exception as e:
                    log.log_error('Error performing a new check: %s' % e.message)

                if data.host_info.key != '':
                    try:
                        online.send_check()
                    except ValueError as e:
                        log.log_error('Unable to send the check to CentralReport Online: %s' % e.message)
                    except errors.OnlineError as e:
                        log.log_error('Error sending the check to CentralReport Online: %s' % e.message)
                    except errors.OnlineNotValidated:
                        log.log_info('This host must be validated on CentralReport Online!')
                    except Exception as e:
                        log.log_error('Unkown error sending the check to CentralReport Online: %s' % e.message)
                else:
                    log.log_debug('User key is not defined: no connection with CentralReport Online available')

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

        # DEPRECATED
        # Only used for the web services. Will be improved soon.
        if data.last_check is not None:
            data.previous_check = copy.copy(data.last_check)

        data.last_check = check_entity

        log.log_debug('All checks are done')
