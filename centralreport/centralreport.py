#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Main
        Entry point of the application. Can be executed with "python centralreport.py start|stop|status"

    https://github.com/miniche/CentralReport/
"""

import datetime
import getpass
import sys
import time
import os

from cr import log
from cr import threads
from cr.utils import text
from cr.daemon import Daemon
from cr.tools import Config


class CentralReport(Daemon):
    is_running = True  # Deamon status
    starting_date = None

    # Threads
    checks_thread = None
    webserver_thread = None

    def run(self):
        """
            Constructor.
        """

        is_error = False  # If True, there are one or more errors when CentralReport is trying to start

        log.log_info('CentralReport is starting...')

        log.log_info('Current user: ' + getpass.getuser())

        CentralReport.starting_date = datetime.datetime.now()  # Starting date
        CentralReport.configuration = Config()  # Getting config object

        # Getting current OS...
        if (Config.HOST_CURRENT == Config.HOST_MAC) or (Config.HOST_CURRENT == Config.HOST_DEBIAN) or (
                Config.HOST_CURRENT == Config.HOST_UBUNTU):
            log.log_info('%s detected. Starting ThreadChecks...' % Config.HOST_CURRENT)
            CentralReport.checks_thread = threads.Checks()  # Launching checks thread
        else:
            is_error = True
            log.log_critical('Sorry, but your OS is not supported yet...')

        # Is webserver enabled?
        if not is_error and text.convert_text_to_bool(Config.get_config_value('Webserver', 'enable')):
            from web.server import WebServer

            log.log_info('Enabling the webserver')
            CentralReport.webserver_thread = WebServer()
        else:
            log.log_info('Webserver is disabled by configuration file')

        if not is_error:
            log.log_info('CentralReport started!')

            while CentralReport.is_running:
                try:
                    if not Config.CR_CONFIG_ENABLE_DEBUG_MODE:
                        # If .pid file is not found, we must stop CR (only in production environment)
                        try:
                            pf = file(self.pidfile, 'r')
                            pf.close()
                        except IOError:
                            log.log_error('Pid file is not found. CentralReport must stop itself.')
                            CentralReport.is_running = False
                            self.stop()
                    time.sleep(1)

                except KeyboardInterrupt:
                    # Stopping CR
                    log.log_critical('KeyboardInterrupt exception. Stopping CentralReport...')
                    CentralReport.is_running = False
                    self.stop()
        else:
            log.log_error('Error launching CentralReport!')

    def stop(self):
        """
            Stops all threads, Daemon and kill CentralReport instance.
        """

        log.log_info('Stopping CentralReport...')
        self.is_running = False

        if CentralReport.webserver_thread is not None:
            log.log_info('Stopping Webserver...')
            CentralReport.webserver_thread.stop()

        if CentralReport.checks_thread is not None:
            log.log_info('Stopping checks thread...')
            threads.Checks.performChecks = False

        log.log_info('Stopping daemon...')

        try:
            Daemon.stop(self)
        except:
            log.log_info('PID file not found.')

        # In test mode, we only return 0 (exit can be personalized by others scripts)
        # But in production, we kill immediately the process.

        if not Config.CR_CONFIG_ENABLE_DEBUG_MODE:
            os.system('kill %d' % os.getpid())

        return 0

    def status(self):
        """
            Checks the status of Central Report and returns the demon PID.
            @return Int: Unix daemon pid ID
        """

        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = 0

        return pid

    def debug(self):
        """
            Function used to launch CentralReport without running the daemon.
            Very useful to run CR in a IDE console
        """

        Config.CR_CONFIG_ENABLE_DEBUG_MODE = True
        log.debug_mode_enabled = True

        self.run()


#
# Main script
#

if '__main__' == __name__:
    daemon = CentralReport(Config.CR_PID_FILE)

    if 2 == len(sys.argv):
        if 'start' == sys.argv[1]:
            daemon.start()

        elif 'stop' == sys.argv[1]:
            daemon.stop()

        elif 'restart' == sys.argv[1]:
            daemon.restart()

        elif 'status' == sys.argv[1]:
            pid = daemon.status()

            if 0 == pid:
                print 'CentralReport is not running'
            else:
                print 'CentralReport is running with pid %s' % pid
        else:
            print 'usage: %s start|stop|restart|status' % sys.argv[0]
            sys.exit(2)
        sys.exit(0)

    else:
        print 'usage: %s start|stop|restart|status' % sys.argv[0]
        sys.exit(2)
