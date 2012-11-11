#
# CentralReport - Indev version
#

import threading,time,datetime
import cr.collectors
from cr.tools import Config

class Checks(threading.Thread):
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
        if Config.HOST_CURRENT == Config.HOST_MAC:
            self.MyCollector = cr.collectors.MacCollector()
        elif(Config.HOST_CURRENT == Config.HOST_DEBIAN) | (Config.HOST_CURRENT == Config.HOST_UBUNTU):
            self.MyCollector = cr.collectors.DebianCollector()

        self.start()


    def run(self):
        """
            Execute checks
        """

        # Getting informations on the current host
        Checks.hostEntity = self.MyCollector.get_infos()

        while Checks.performChecks:

            print("---- New check -----")
            print("Date : "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Checks CPU
            if Config.config_enable_check_cpu:
                # Oui, on procede au releve CPU
                print("Do a CPU check...")
                Checks.last_check_cpu = self.MyCollector.get_cpu()

            # Check memoire
            if Config.config_enable_check_memory:
                print("Do a memory check...")
                Checks.last_check_memory = self.MyCollector.get_memory()

            # Check Load Average
            if Config.config_enable_check_loadaverage:
                print("Do a load average check...")
                Checks.last_check_loadAverage = self.MyCollector.get_loadaverage()

            #Checking disks informations
            print("Do a disk check....")
            Checks.last_check_disk = self.MyCollector.get_disks()

            # Update the last check date
            Checks.last_check_date = datetime.datetime.now()

            # Wait 60 seconds before next checks...
            print("All checks are done at : "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("Next checks in 60 seconds...")
            time.sleep(60)