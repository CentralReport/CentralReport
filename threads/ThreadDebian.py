__author__ = 'che'

from collectors.DebianCollector import DebianCollector
from network.speaker import Speaker
from utils.config import ConfigGetter
import time

class ThreadDebian:

    def __init__(self):
        print ("Thread Debian is ready")
        # On definit notre collecteur de donnees pour mac
        self.MyCollector = DebianCollector()

        # Ready to go !
        # On enregistre la machine
        dict_machine = self.MyCollector.getInfos()

        Speaker.sendStats(Speaker.page_INFOS,dict_machine)

        # Et on boucle a l'infini pour envoyer nos stats
        while True:

            # Checks CPU
            if ConfigGetter.config_enable_check_cpu:
                # Oui, on procede au releve CPU
                print("DO A CPU CHECK...")
                dict_cpu = self.MyCollector.getCPU()
                dict_cpu['uuid'] = ConfigGetter.ident
                Speaker.sendStats(Speaker.page_CPU,dict_cpu)

            # Check memoire
            if ConfigGetter.config_enable_check_memory:
                print("DO A MEMORY CHECK")
                dict_memory = self.MyCollector.getMemory()
                dict_memory['uuid'] = ConfigGetter.ident
                Speaker.sendStats(Speaker.page_MEMORY,dict_memory)

            # Check Load Average
            if ConfigGetter.config_enable_check_loadaverage:
                print("DO A LOADAVG CHECK")
                dict_loadavg = self.MyCollector.getLoadAverage()
                dict_loadavg['uuid'] = ConfigGetter.ident
                Speaker.sendStats(Speaker.page_LOADAVERAGE,dict_loadavg)


            # Et on attend une petite minute
            print("NEXT PASS IN 60 SECONDS")
            time.sleep(60)