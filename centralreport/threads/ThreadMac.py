# CentralReport - Indev version


import time, threading, datetime

from collectors.MacCollector import MacCollector
from network.speaker import Speaker
from utils.config import ConfigGetter


class ThreadMac(threading.Thread):
    """
    This thread can do periodic checks on the system (Mac OS X host only)
    """

    # Get host informations
    hostEntity = None

    # Last checks (with new entities classes)
    last_check_date = None
    last_check_cpu = None
    last_check_memory = None
    last_check_loadAverage = None
    last_check_disk = None

    def __init__(self):
        threading.Thread.__init__(self)

        # Sortie standard
        print ("Thread MacOS is ready")

        # On definit notre collecteur de donnees pour mac
        self.MyCollector = MacCollector()


    def run(self):
        # Ready to go !
        # On enregistre la machine
        ThreadMac.hostEntity = self.MyCollector.getInfos()

        #Speaker.sendStats(Speaker.page_INFOS,ThreadMac.dict_machine)


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
            ThreadMac.last_check_disk = self.MyCollector.getDisksInfo()

            # Update the last check date
            ThreadMac.last_check_date = datetime.datetime.now()

            # Wait 60 seconds before next checks...
            print("Next checks in 60 seconds...")
            time.sleep(60)