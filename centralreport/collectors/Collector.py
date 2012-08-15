__author__ = 'che'

import subprocess, os

class Collector:

    # Machine actuelle
    host_current = ""

    # Constantes de configuration
    host_MacOS = "Mac OS X"
    host_Linux = "Linux"
    host_Debian = "Debian"
    host_Ubuntu = "Ubuntu"
    host_RedHat = "RedHat"
    host_Fedora = "Fedora"

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

            # On va essayer d'affiner en fonction des distributions

            # Removed : On va etre encore plus malin que ca !
#            distrib_linux = subprocess.Popen(['cat','/etc/issue'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
#            if "Debian" in distrib_linux:
#                # C'est une Debian
#                Collector.host_current = Collector.host_Debian
#            elif "Fedora" in distrib_linux:
#                # Fedora
#                Collector.host_current = Collector.host_Fedora

            # Utilisation de la liste de Novell pour reconnaitre des distrib Linux
            # http://www.novell.com/coolsolutions/feature/11251.html

            if os.path.isfile("/etc/lsb-release"):
                # Ubuntu !
                Collector.host_current = Collector.host_Ubuntu
            elif os.path.isfile("/etc/debian_version"):
                # Une Debian pure et dure dans ce cas !
                Collector.host_current = Collector.host_Debian
            elif os.path.isfile("/etc/fedora-release"):
                # Fedora !
                Collector.host_current = Collector.host_Fedora
            elif os.path.isfile("/etc/redhat_version"):
                # RedHat !
                Collector.host_current = Collector.host_RedHat


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