# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import threading
import utils.log, utils.config
from utils.config import ConfigGetter
from collectors.Collector import Collector
from threads.ThreadMac import ThreadMac
from threads.ThreadDebian import ThreadDebian

class CentralReport:

    def __init__(self):
        # Constructeur
        utils.log.CRLog.writeLog("CentralReport -- RUN")

        # Ce constructeur va permettre de lancer l'ensemble des outils necessaires
        #Premiere chose : regarde l'OS actuel
        Collector.getCurrentHost()

        # Deuxieme chose : la configuration via le fichier de conf.
        configuration = ConfigGetter()

        #idMachine = utils.config.configGetter.config.get("General","id")
        #utils.log.CRLog.writeLog("UUID : "+ str(idMachine))

        # Quel thread doit-on lancer ?
        if Collector.host_current == Collector.host_MacOS:
            # C'est un mac ! Bon gars :)
            print("Mac detected. Start ThreadMac")
            threading.Thread(None,ThreadMac())
        elif Collector.host_current == Collector.host_Debian | Collector.host_current == Collector.host_Ubuntu:
            # Distrib Debian ou Ubuntu. Aller, ca reste un assez bon gars ca :)
            print(Collector.host_current +" detected. Start ThreadDebian")
            threading.Thread(None,ThreadDebian())
        else:
            print("Sorry, but your distrib is not supported")