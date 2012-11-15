#!/usr/bin/python

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import sys
import time
import datetime
import cr.log crLog
import cr.threads crThreads
from cr.tools import Config
from daemon import Daemon
from web.server import WebServer


class CentralReport(Daemon):
    # Bool : True = daemon is running.
    isRunning = True
    startingDate = None
    configuration = None

    def run(self):
        # Constructeur

        # False = no error
        isError = False

        # On prepare les logs
        crLog.configLog()
        crLog.writeInfo("CentralReport is starting...")

        # Starting date
        CentralReport.startingDate = datetime.datetime.now()

        # Ce constructeur va permettre de lancer l'ensemble des outils necessaires
        CentralReport.configuration = Config()
        #idMachine = utils.config.configGetter.config.get("General","id")
        #utils.log.CRLog.writeLog("UUID : "+ str(idMachine))

        # Quel thread doit-on lancer ?
        if (Config.HOST_CURRENT == Config.HOST_MAC) | (Config.HOST_CURRENT == Config.HOST_DEBIAN) | (
        Config.HOST_CURRENT == Config.HOST_UBUNTU):
            print(Config.HOST_CURRENT + " detected. Starting ThreadChecks...")

            # Lancement thread
            crThreads.Checks()

        else:
            isError = True
            print("Sorry, but your OS is not supported yet...")

        # Enable webserver ?
        if (Config.config_webserver_enable) & (not isError):
            # Yeah !
            print("Enabling the webserver")

            WebServer()

        else:
            print("Webserver is disabled by configuration file")
            crLog.writeInfo("Webserver is disabled by configuration file")

        # End of file
        if(not isError):
            crLog.writeInfo("CentralReport started!")

            while self.isRunning:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    # Stopping CR
                    print("KeyboardInterrupt exception. Stopping CentralReport...")
                    self.isRunning = False
                    self.stop()

        else:
            crLog.writeError("Error launching CentralReport!")

    def stop(self):
        """
            Called when the scripts will be stopped
        """

        crLog.writeInfo("Stopping CentralReport...")

        self.isRunning = False
        Daemon.stop(self)

        # Stopping CR...
        sys.exit(0)


#
# Main script
#

if __name__ == "__main__":
    daemon = CentralReport(Config.pid_file)

    if 2 == len(sys.argv):
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'develop' == sys.argv[1]:
            # With develop option, we only starting CR, without the daemonizer.
            daemon.run()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
