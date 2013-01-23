#!/usr/bin/python
# -*- coding: utf-8 -*-

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import cr.log as crLog
import cr.threads as crThreads
import cr.utils.text as crUtilsText
import datetime
import sys
import time
import os
from cr.daemon import Daemon
from cr.tools import Config
from web.server import WebServer


class CentralReport(Daemon):

    isRunning = True  # Deamon status
    startingDate = None

    # Threads

    checks_thread = None
    webserver_thread = None

    def run(self):
        """
            Constructor.
        """

        isError = False  # If True, there are one or more errors when CentralReport is trying to start

        # Preparing Logs

        crLog.configLog(Config.CR_CONFIG_ENABLE_DEBUG_MODE)
        crLog.writeInfo('CentralReport is starting...')

        CentralReport.startingDate = datetime.datetime.now()  # Starting date
        CentralReport.configuration = Config()  # Getting config object

        # Getting current OS...
        if (Config.HOST_CURRENT == Config.HOST_MAC) | (Config.HOST_CURRENT == Config.HOST_DEBIAN) | (
        Config.HOST_CURRENT == Config.HOST_UBUNTU):
            crLog.writeInfo(Config.HOST_CURRENT + ' detected. Starting ThreadChecks...')
            CentralReport.checks_thread = crThreads.Checks()  # Launching checks thread
        else:
            isError = True
            crLog.writeCritical('Sorry, but your OS is not supported yet...')

        # Is webserver enabled ?
        if not isError & crUtilsText.textToBool(Config.getConfigValue('Webserver', 'enable')):
            crLog.writeInfo('Enabling the webserver')
            CentralReport.webserver_thread = WebServer()
        else:
            crLog.writeInfo('Webserver is disabled by configuration file')

        if not isError:
            crLog.writeInfo('CentralReport started!')

            while CentralReport.isRunning:
                try:

                    if not Config.CR_CONFIG_ENABLE_DEBUG_MODE:

                        # If .pid file is not found, we must stop CR (only in production environment)

                        try:
                            pf = file(self.pidfile, 'r')
                            pf.close()
                        except IOError:
                            crLog.writeError('Pid file is not found. CentralReport must stop itself.')
                            CentralReport.isRunning = False
                            self.stop()

                    time.sleep(1)
                except KeyboardInterrupt:

                    # Stopping CR

                    crLog.writeFatal('KeyboardInterrupt exception. Stopping CentralReport...')
                    CentralReport.isRunning = False
                    self.stop()
        else:

            crLog.writeError('Error launching CentralReport!')

    def stop(self):
        """
            Stops all threads, Daemon and kill CentralReport instance.
        """

        crLog.writeInfo('Stopping CentralReport...')
        self.isRunning = False

        if CentralReport.webserver_thread is not None:
            crLog.writeInfo('Stopping Webserver...')
            CentralReport.webserver_thread.stop()

        if CentralReport.checks_thread is not None:
            crLog.writeInfo('Stopping checks thread...')
            crThreads.Checks.performChecks = False

        crLog.writeInfo('Stopping daemon...')

        try:
            Daemon.stop(self)
        except:
            crLog.writeInfo('PID file not found.')

        # In test mode, we only return 0 (exit can be personalized by others scripts)
        # But in production, we kill immediately the process.

        if not Config.CR_CONFIG_ENABLE_DEBUG_MODE:
            os.system('kill %d' % os.getpid())

        return 0

    def status(self):
        """
            Checks the status of Central Report and returns the demon PID.
            @return Int : Unix daemon pid ID
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
            Very useful to run CR in a IDE console :)
        """

        Config.CR_CONFIG_ENABLE_DEBUG_MODE = True
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
                print 'CentralReport is running with pid ' + str(pid)
        else:

            crLog.writeError('Unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        crLog.writeError("usage: %s start|stop|restart|status" % sys.argv[0])
        sys.exit(2)
