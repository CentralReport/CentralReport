# -*- coding: utf-8 -*-

"""
    CentralReport - Threads module
        Contains threads used by CentralReport to perform periodic actions

    https://github.com/miniche/CentralReport/
"""

from datetime import datetime
import json
import threading
import time

from cr import collectors
from cr import log
from cr.entities import checks
from cr.tools import Config
from cr import webservices


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
    is_registered = False

    route_main = ''
    route_hosts = ''
    route_checks = ''

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
                # Checking if this host is already registred on the remote server
                log.log_info('A key is defined for the remote server!')

                if Remote.route_hosts == '':
                    Remote.route_main = Config.CR_REMOTE_ROUTE.replace('%key%', Checks.host_infos.key)
                    ws_user = webservices.send_data(webservices.METHOD_GET, Remote.route_main, None, None)

                    if ws_user.code == 404:
                        log.log_error('The key %s is not a valid key on the remote server!' % Checks.host_infos.key)
                    elif ws_user.code != 200 or ws_user.headers.count('application/json') == 0:
                        log.log_error('The server has returned a unknown response.')
                        log.log_error('Code: %s - Content: %s' % (ws_user.code, ws_user.text))
                    else:
                        # This key seems valid! Getting all routes available with HATEOAS
                        try:
                            remote_json = json.loads(ws_user.text)
                            Remote.route_hosts = remote_json['routes']['hosts']
                        except:
                            log.log_error('Error reading the JSON returned by the remote server!')
                            Remote.route_hosts = ''

                if Remote.route_hosts != '':
                    # We can now check if the current host is registered on the remote server
                    Remote.route_hosts = Remote.route_hosts.replace('%uuid%', Checks.last_check.uuid)
                    ws_host = webservices.send_data(webservices.METHOD_GET, Remote.route_main, None, None)

                    if ws_host.code == 401:
                        log.log_info('Please validate this host on the remote server!')
                        Remote.route_checks = ''
                    elif ws_host.code == 200:
                        log.log_info('Host registered on the remote server')

                        try:
                            remote_json = json.loads(ws_host.text)
                            Remote.route_checks = remote_json['routes']['checks']
                        except:
                            log.log_error('Error reading the JSON returned by the remote server!')
                            Remote.route_checks = ''

                    elif ws_host.code == 404:
                        log.log_info('Host not registered. Registering this host the the remote server...')
                        # TODO: Using the new serializer, send host data to the remote server


                if Remote.route_hosts != '' and Remote.route_checks != '':
                    # Ok, we can send checks to the remote server!
                    # TODO: Using the new serializer, send checks to the remote server
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
