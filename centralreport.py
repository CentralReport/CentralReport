# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import threading
import utils.log, utils.config
from utils.config import ConfigGetter
from collectors.Collector import Collector
from threads.ThreadMac import ThreadMac

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
        if Collector.isMac():
            # C'est un mac ! Bon gars :)
            print("Mac detected. Start ThreadMac")
            threading.Thread(None,ThreadMac())