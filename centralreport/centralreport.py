#!/usr/bin/python

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import sys
import time
import datetime
import cr.log as crLog
import cr.threads as crThreads
from cr.tools import Config
from cr.daemon import Daemon
from web.server import WebServer


class CentralReport(Daemon):
    # Bool : True = daemon is running.
    isRunning = True
    startingDate = None

    # Configuration object
    configuration = None

    # Threads
    webserver_thread = None
    checks_thread = None


    def run(self):
        # Constructeur

        # False = no error
        isError = False

        # On prepare les logs
        crLog.configLog(Config.CR_CONFIG_ENABLE_DEBUG_MODE)
        crLog.writeInfo("CentralReport is starting...")

        # Starting date
        CentralReport.startingDate = datetime.datetime.now()

        # Getting config object
        CentralReport.configuration = Config()

        # Getting current OS...
        if (Config.HOST_CURRENT == Config.HOST_MAC) | (Config.HOST_CURRENT == Config.HOST_DEBIAN) | (
        Config.HOST_CURRENT == Config.HOST_UBUNTU):
            crLog.writeInfo(Config.HOST_CURRENT + " detected. Starting ThreadChecks...")

            # Launching checks thread
            CentralReport.checks_thread = crThreads.Checks()

        else:
            isError = True
            crLog.writeCritical("Sorry, but your OS is not supported yet...")

        # Enable webserver ?
        if (Config.getConfigValue('enable','Webserver')) & (not isError):
            # Yeah !
            crLog.writeInfo("Enabling the webserver")

            CentralReport.webserver_thread = WebServer()

        else:
            crLog.writeInfo("Webserver is disabled by configuration file")


        #
        if(not isError):
            crLog.writeInfo("CentralReport started!")

            while CentralReport.isRunning:
                try:

                    if Config.CR_CONFIG_ENABLE_DEBUG_MODE == False:
                        # If .pid file is not found, we must stop CR (only in production environement)
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
                    crLog.writeFatal("KeyboardInterrupt exception. Stopping CentralReport...")
                    CentralReport.isRunning = False
                    self.stop()

        else:
            crLog.writeError("Error launching CentralReport!")


    def stop(self):
        """
            Called when the scripts will be stopped
        """
        crLog.writeInfo("Stopping CentralReport...")
        self.isRunning = False

        if None != CentralReport.webserver_thread:
            crLog.writeInfo('Stopping Webserver...')
            CentralReport.webserver_thread.stop()

        if None != self.checks_thread:
            crLog.writeInfo('Stopping checks thread...')
            crThreads.Checks.performChecks = False

        crLog.writeInfo("Stopping daemon...")

        try:
            Daemon.stop(self)
        except:
            crLog.writeInfo("Pid file not found.")

        return 0


    def status(self):
        """
            CentralReport is running ?
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
            Use this function to launch CentralReport without running the daemon.
            Very useful to run CR in a IDE console :)
        """

        Config.CR_CONFIG_ENABLE_DEBUG_MODE = True
        self.run()

#
# Main script
#

if __name__ == "__main__":
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
            if 0 == pid :
                print('CentralReport is not running')
            else:
                print('CentralReport is running with pid '+ str(pid))

        else:
            crLog.writeError("Unknown command")
            sys.exit(2)
        sys.exit(0)

    else:
        crLog.writeError("usage: %s start|stop|restart|status" % sys.argv[0])
        sys.exit(2)
