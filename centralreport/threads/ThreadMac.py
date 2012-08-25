__author__ = 'che'

from collectors.MacCollector import MacCollector
from network.speaker import Speaker
from utils.config import ConfigGetter
import time
import threading

class ThreadMac(threading.Thread):

    # Last checks
    dict_machine = []
    last_dict_cpu = []
    last_dict_memory = []
    last_dict_loadavg = []
    last_list_disk = []

    def __init__(self):
        threading.Thread.__init__(self)

        # Sortie standard
        print ("Thread MacOS is ready")

        # On definit notre collecteur de donnees pour mac
        self.MyCollector = MacCollector()


    def run(self):
        # Ready to go !
        # On enregistre la machine
        ThreadMac.dict_machine = self.MyCollector.getInfos()

        Speaker.sendStats(Speaker.page_INFOS,ThreadMac.dict_machine)

        # Et on boucle a l'infini pour envoyer nos stats
        while True:

            # Checks CPU
            if ConfigGetter.config_enable_check_cpu:
                # Oui, on procede au releve CPU
                print("DO A CPU CHECK...")
                ThreadMac.last_dict_cpu = self.MyCollector.getCPU()
                ThreadMac.last_dict_cpu['uuid'] = ConfigGetter.uuid
                #Speaker.sendStats(Speaker.page_CPU,ThreadMac.last_dict_cpu)

            # Check memoire
            if ConfigGetter.config_enable_check_memory:
                print("DO A MEMORY CHECK")
                ThreadMac.last_dict_memory = self.MyCollector.getMemory()
                ThreadMac.last_dict_memory['uuid'] = ConfigGetter.uuid
                #Speaker.sendStats(Speaker.page_MEMORY,ThreadMac.last_dict_memory)

            # Check Load Average
            if ConfigGetter.config_enable_check_loadaverage:
                print("DO A LOADAVG CHECK")
                ThreadMac.last_dict_loadavg = self.MyCollector.getLoadAverage()
                ThreadMac.last_dict_loadavg['uuid'] = ConfigGetter.uuid
                #Speaker.sendStats(Speaker.page_LOADAVERAGE,ThreadMac.last_dict_loadavg)

            #Checking disks informations
            print("DO A DISK CHECK")
            ThreadMac.last_list_disk = self.MyCollector.getDisksInfo()


            # Et on attend une petite minute
            time.sleep(60)