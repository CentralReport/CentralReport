#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    CentralReport - Main
        Entry point of the application. Can be executed with "python centralreport.py start|stop|status"

    https://github.com/CentralReport
"""

import datetime
import getpass
import signal
import sys
import time
import os

import cr.libs
cr.libs.register_libraries()

from cr import host
from cr import log
from cr import threads
from cr.utils import text
from cr.daemon import Daemon
from cr.tools import Config
from cr.utils import web as utils_web


class CentralReport(Daemon):
    is_running = True  # Deamon status
    starting_date = None

    # Threads
    checks_thread = None
    remote_thread = None
    webserver_thread = None

    # Sigterm signal
    SIGTERM_SENT = False

    def signal_handler(self, signum, frame):
        """
            Receives signals from the OS.
        """

        if signum == signal.SIGTERM:
            # In this case, we must stop CentralReport immediatly!
            if not self.SIGTERM_SENT:
                self.SIGTERM_SENT = True  # Prevents if SIGTERM is received twice.

                log.log_info('SIGTERM signal received (%s). Shutting Down...' % signum)
                log.log_info('Shutting down sub-processes...')
                os.killpg(0, signal.SIGTERM)

                self.stop()

        elif signum == signal.SIGINT:
            # Keyboard interruption (CTRL + C)
            log.log_info('SIGINT signal received (%s). Stopping CentralReport...' % signum)
            self.stop()

        else:
            log.log_debug('Unknown signal number: %s' % signum)

    def run(self):
        """
            Constructor.
        """

        is_error = False  # If True, there are one or more errors when CentralReport is trying to start

        log.log_info('------------------------------------------------')
        log.log_info('CentralReport is starting...')
        log.log_info('Current user: ' + getpass.getuser())

        # Registering SIGTERM signal event
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        CentralReport.starting_date = datetime.datetime.now()
        CentralReport.configuration = Config()

        host.get_current_host()

        # The log level can be personalized in the config file
        if Config.CR_CONFIG_ENABLE_DEBUG_MODE is False:
            try:
                log_level = Config.get_config_value('Debug', 'log_level')
            except:
                log_level = 'INFO'

            log.change_log_level(log_level)

        # Starting the check thread...
        if host.get_current_host().os != host.OS_UNKNOWN:
            log.log_info('%s detected. Starting ThreadChecks...' % host.get_current_host().os)
            CentralReport.checks_thread = threads.Checks()  # Launching checks thread
        else:
            is_error = True
            log.log_critical('Sorry, but your OS is not supported yet...')

        # Starting the internal webserver...
        if not is_error and text.convert_text_to_bool(Config.get_config_value('Webserver', 'enable')):
            local_web_port = int(Config.get_config_value('Webserver', 'port'))

            if not utils_web.check_port('127.0.0.1', local_web_port):
                log.log_info('Starting the webserver...')

                # Importing the module here improve the memory usage
                from web.server import WebServer

                CentralReport.webserver_thread = WebServer()
            else:
                log.log_error('Error launching the webserver: port %s is already in use on this host!' % local_web_port)
        else:
            log.log_info('Webserver is disabled by configuration file!')

        if not is_error:
            log.log_info('CentralReport started!')

            while CentralReport.is_running:
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

        log.log_info('A last word from the daemon: Bye!')

        # Killing the current processus...
        # (This command send the "SIGKILL" signal)
        os.system('kill -9 %d' % os.getpid())

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

    def modify_config(self, key, value):
        """
            Modifies one value in the config file
        """

        cr_config = Config()
        array_key = key.split(':')

        try:
            Config.set_config_value(array_key[0], array_key[1], value)
        except Exception as e:
            print(e.message)
            return False

        try:
            cr_config.write_config_file()
        except Exception as e:
            print(e.message)
            return False

        return True



#
# Main script
#

if '__main__' == __name__:

    if sys.version_info < (2, 6):
        print "CentralReport works only with Python 2.6 or newer."
        sys.exit(1)
    elif sys.version_info >= (3, 0):
        print "CentralReport doesn't work with Python 3.0 or newer."
        sys.exit(1)

    daemon = CentralReport(Config.CR_PID_FILE)

    if len(sys.argv) > 1:
        if 'start' == sys.argv[1]:
            daemon.start()

        elif 'stop' == sys.argv[1]:
            daemon.stop()

        elif 'config' == sys.argv[1]:
            if daemon.modify_config(sys.argv[2], sys.argv[3]) is False:
                sys.exit(2)

        else:
            print 'usage: %s start|stop|config' % sys.argv[0]
            sys.exit(2)
    else:
        print 'usage: %s start|stop|config' % sys.argv[0]
        sys.exit(2)

    sys.exit(0)
