# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import utils.log, utils.config
from utils.config import ConfigGetter
from collectors.Collector import Collector
from threads.ThreadMac import ThreadMac
from threads.ThreadDebian import ThreadDebian
from web.webserver import WebServer

class CentralReport:

    def __init__(self):
        # Constructeur

        # On prepare les logs
        utils.log.CRLog.configLog()
        utils.log.CRLog.writeInfo("CentralReport is starting...")

        # Ce constructeur va permettre de lancer l'ensemble des outils necessaires
        # Premiere chose : regarde l'OS actuel
        Collector.getCurrentHost()

        # Deuxieme chose : la configuration via le fichier de conf.
        configuration = ConfigGetter()

        #idMachine = utils.config.configGetter.config.get("General","id")
        #utils.log.CRLog.writeLog("UUID : "+ str(idMachine))

        # Quel thread doit-on lancer ?
        if Collector.host_current == Collector.host_MacOS:
            # C'est un mac ! Bon gars :)
            print("Mac detected. Start ThreadMac")
            # Lancement thread
            ThreadMac().start()

        elif Collector.host_current == Collector.host_Debian | Collector.host_current == Collector.host_Ubuntu:
            # Distrib Debian ou Ubuntu. Aller, ca reste un assez bon gars ca :)
            print(Collector.host_current +" detected. Start ThreadDebian")
            # Lancement thread
            ThreadDebian().start()

        else:
            print("Sorry, but your distrib is not supported")


        # Enable webserver ?
        if ConfigGetter.config_webserver_enable == True:
            # Yeah !
            print("Enabling the webserver")
            WebServer().start()
            #WebServer()

        else:
            print("Webserver is disabled by configuration file")
            utils.log.CRLog.writeInfo("Webserver is disabled by configuration file")



        # End of file
        utils.log.CRLog.writeInfo("CentralReport started!")


    def stop(self):
        """
        Called when the scripts will be stopped
        """

        utils.log.CRLog.writeInfo("Stopping CentralReport")