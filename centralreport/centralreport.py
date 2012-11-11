#!/usr/bin/python

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import sys,time,datetime
import cr.log, cr.threads
from cr.tools import Config
from daemon import Daemon
from web.server import WebServer

class CentralReport(Daemon):

    # Bool : True = daemon is running.
    isRunning = True
    startingDate = None

    def run(self):
        # Constructeur

        # False = no error
        isError = False

        # On prepare les logs
        cr.log.configLog()
        cr.log.writeInfo("CentralReport is starting...")

        # Starting date
        CentralReport.startingDate = datetime.datetime.now()

        # Ce constructeur va permettre de lancer l'ensemble des outils necessaires

        # Deuxieme chose : la configuration via le fichier de conf.
        configuration = Config()

        #idMachine = utils.config.configGetter.config.get("General","id")
        #utils.log.CRLog.writeLog("UUID : "+ str(idMachine))

        # Quel thread doit-on lancer ?
        if (Config.HOST_CURRENT == Config.HOST_MAC) | (Config.HOST_CURRENT == Config.HOST_DEBIAN) | (Config.HOST_CURRENT == Config.HOST_UBUNTU):
            print(Config.HOST_CURRENT +" detected. Starting ThreadChecks...")

            # Lancement thread
            cr.threads.Checks()

        else:
            isError = True
            print("Sorry, but your OS is not supported yet...")


        # Enable webserver ?
        if (Config.config_webserver_enable == True) & (isError == False):
            # Yeah !
            print("Enabling the webserver")

            WebServer()

        else:
            print("Webserver is disabled by configuration file")
            cr.log.writeInfo("Webserver is disabled by configuration file")

        # End of file
        if(isError == False):
            cr.log.writeInfo("CentralReport started!")

            while self.isRunning:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    # Stopping CR
                    print("KeyboardInterrupt exception. Stopping CentralReport...")
                    self.isRunning = False
                    self.stop()

        else:
           cr.log.writeError("Error launching CentralReport!")

    def stop(self):
        """
        Called when the scripts will be stopped
        """

        cr.log.writeInfo("Stopping CentralReport...")

        self.isRunning = False
        Daemon.stop(self)

        # Stopping CR...
        sys.exit(0)


#
# Main script
#

if __name__ == "__main__":

    # Launching the daemon...
    daemon = CentralReport(Config.pid_file)

    if len(sys.argv) == 2:
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