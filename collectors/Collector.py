__author__ = 'che'

import subprocess

class Collector:

    # Machine actuelle
    host_current = ""

    # Constantes de configuration
    host_MacOS = "Mac OS X"
    host_Linux = "Linux"

    @staticmethod
    def getCurrentHost():
        """
        Permet d'obtenir le type de machine actuel
        """

        # Est-ce un mac ?
        kernel_mac = subprocess.Popen(['sysctl','-n','kern.ostype'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        kernel_linux = subprocess.Popen(['sysctl','-n','kernel.ostype'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        #print(str(kernel_mac))
        if kernel_mac.startswith("Darwin"):
            # Yes, it's a beautiful Mac !
            Collector.host_current = Collector.host_MacOS
        elif kernel_linux.startswith("Linux"):
            # Non ? On est sur linux !
            Collector.host_current = Collector.host_Linux

        return Collector.host_current


    @staticmethod
    def isMac():
        """
            Permet de savoir si le systeme actuel est un Mac
        """
        if Collector.host_current == Collector.host_MacOS:
            return True
        else:
            return False