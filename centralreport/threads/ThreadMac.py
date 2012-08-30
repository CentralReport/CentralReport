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

    # Last checks (with new entities classes)
    last_check_cpu = None
    last_check_memory = None
    last_check_loadAverage = None

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
                ThreadMac.last_check_cpu = self.MyCollector.getCPU()

            # Check memoire
            if ConfigGetter.config_enable_check_memory:
                print("DO A MEMORY CHECK")
                ThreadMac.last_check_memory = self.MyCollector.getMemory()

            # Check Load Average
            if ConfigGetter.config_enable_check_loadaverage:
                print("DO A LOADAVG CHECK")
                ThreadMac.last_check_loadAverage = self.MyCollector.getLoadAverage()

            #Checking disks informations
            print("DO A DISK CHECK")
            ThreadMac.last_list_disk = self.MyCollector.getDisksInfo()


            # Et on attend une petite minute
            print("Next checks in 60 seconds...")
            time.sleep(60)