#
# CentralReport - Indev version
#

import threading,time,datetime
import collectors.Collector,collectors.DebianCollector,collectors.MacCollector
from utils.CRConfig import CRConfig

class ThreadChecks(threading.Thread):
    """
        This thread will perform periodically checks.
    """


    # True = perform checks...
    performChecks = True

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
        print ("ThreadChecks is starting...")

        # What is the current os ?
        if CRConfig.HOST_CURRENT == CRConfig.HOST_MAC:
            self.MyCollector = collectors.MacCollector.MacCollector()
        elif(CRConfig.HOST_CURRENT == CRConfig.HOST_DEBIAN) | (CRConfig.HOST_CURRENT == CRConfig.HOST_UBUNTU):
            self.MyCollector = collectors.DebianCollector.DebianCollector()

        self.start()


    def run(self):
        """
            Execute checks
        """

        # Getting informations on the current host
        ThreadChecks.hostEntity = self.MyCollector.get_infos()

        while ThreadChecks.performChecks:

            print("---- New check -----")
            print("Date : "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Checks CPU
            if CRConfig.config_enable_check_cpu:
                # Oui, on procede au releve CPU
                print("Do a CPU check...")
                ThreadChecks.last_check_cpu = self.MyCollector.get_cpu()

            # Check memoire
            if CRConfig.config_enable_check_memory:
                print("Do a memory check...")
                ThreadChecks.last_check_memory = self.MyCollector.get_memory()

            # Check Load Average
            if CRConfig.config_enable_check_loadaverage:
                print("Do a load average check...")
                ThreadChecks.last_check_loadAverage = self.MyCollector.get_loadaverage()

            #Checking disks informations
            print("Do a disk check....")
            ThreadChecks.last_check_disk = self.MyCollector.get_disks()

            # Update the last check date
            ThreadChecks.last_check_date = datetime.datetime.now()

            # Wait 60 seconds before next checks...
            print("All checks are done at : "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("Next checks in 60 seconds...")
            time.sleep(60)