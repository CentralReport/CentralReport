#!/usr/bin/python

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import utils.CRLog, utils.CRConfig
from utils.CRConfig import CRConfig
from threads.ThreadChecks import ThreadChecks
from web.webserver import WebServer

class CentralReport():

    def __init__(self):
        # Constructeur

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
            print("Sorry, but your OS is not supported yet...")


        # Enable webserver ?
        if CRConfig.config_webserver_enable == True:
            # Yeah !
            print("Enabling the webserver")
            #WebServer().start()
            WebServer()

        else:
            print("Webserver is disabled by configuration file")
            utils.CRLog.CRLog.writeInfo("Webserver is disabled by configuration file")




        # End of file
        utils.CRLog.CRLog.writeInfo("CentralReport started!")


    def stop(self):
        """
        Called when the scripts will be stopped
        """

        utils.CRLog.CRLog.writeInfo("Stopping CentralReport")