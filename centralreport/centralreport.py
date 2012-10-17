#!/usr/bin/python

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import sys,time,utils.CRLog, utils.CRConfig
from daemon import Daemon
from utils.CRConfig import CRConfig
from threads.ThreadChecks import ThreadChecks
from web.webserver import WebServer

class CentralReport(Daemon):

    # Bool : True = daemon is running.
    isRunning = True

    def run(self):
        # Constructeur

        # False = no error
        isError = False

        # On prepare les logs
        utils.CRLog.CRLog.configLog()
        utils.CRLog.CRLog.writeInfo("CentralReport is starting...")

        # Ce constructeur va permettre de lancer l'ensemble des outils necessaires

        # Deuxieme chose : la configuration via le fichier de conf.
        configuration = CRConfig()

        #idMachine = utils.config.configGetter.config.get("General","id")
        #utils.log.CRLog.writeLog("UUID : "+ str(idMachine))

        # Quel thread doit-on lancer ?
        if (CRConfig.HOST_CURRENT == CRConfig.HOST_MAC) | (CRConfig.HOST_CURRENT == CRConfig.HOST_DEBIAN) | (CRConfig.HOST_CURRENT == CRConfig.HOST_UBUNTU):
            print(CRConfig.HOST_CURRENT +" detected. Starting ThreadChecks...")

            # Lancement thread
            ThreadChecks()

        else:
            isError = True
            print("Sorry, but your OS is not supported yet...")


        # Enable webserver ?
        if (CRConfig.config_webserver_enable == True) & (isError == False):
            # Yeah !
            print("Enabling the webserver")
            #WebServer().start()
            WebServer()

        else:
            print("Webserver is disabled by configuration file")
            utils.CRLog.CRLog.writeInfo("Webserver is disabled by configuration file")

        # End of file
        if(isError == False):
            utils.CRLog.CRLog.writeInfo("CentralReport started!")

            while self.isRunning:
                time.sleep(1)

        else:
            utils.CRLog.CRLog.writeError("Error launching CentralReport!")


    def stop(self):
        """
        Called when the scripts will be stopped
        """

        utils.CRLog.CRLog.writeInfo("Stopping CentralReport...")

        self.isRunning = False
        Daemon.stop(self)


#
# Main script
#

if __name__ == "__main__":

    # Launching the daemon...
    daemon = CentralReport(utils.CRConfig.CRConfig.pid_file)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("CentralReport -- Start")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            print("CentralReport -- Stopped")
        elif 'restart' == sys.argv[1]:
            print ("CentralReport -- Restarting...")
            daemon.restart()
            print ("CentralReport -- Started")
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)