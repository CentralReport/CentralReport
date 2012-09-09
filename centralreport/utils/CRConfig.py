# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

__author__ = 'che'

import ConfigParser, os, uuid, subprocess

class CRConfig:

    config = ConfigParser.ConfigParser()

    uuid = ""
    config_enable_check_memory = True
    config_enable_check_cpu = True
    config_enable_check_loadaverage = True
    config_server_addr = ""

    # CherryPy webserver config
    config_webserver_enable = True
    config_webserver_interface = '0.0.0.0'
    config_webserver_port = 8080


    # Current host
    HOST_CURRENT = ""
    # Some hosts...
    HOST_MAC = "Mac OS X"
    HOST_LINUX = "Linux"
    HOST_DEBIAN = "Debian"
    HOST_UBUNTU = "Ubuntu"
    HOST_REDHAT = "RedHat"
    HOST_FEDORA = "Fedora"


    def __init__(self):

         # Determining current host/os
        CRConfig.determine_current_host()

        if CRConfig.HOST_CURRENT == CRConfig.HOST_MAC:
            # On est sur Mac. Test du repertoire
            if os.path.isdir("/etc/cr") != True:
                # Creation du dossier
                os.mkdir("/etc/cr")

            CRConfig.chemin = "/etc/cr/"
            print("Mac config")
        else:
            # On est sur un systeme Linux

            if os.path.isdir("/etc/cr") != True:
                # Creation du dossier
                os.mkdir("/etc/cr")
            CRConfig.chemin = "/etc/cr/"
            print("Linux config")


        # Fichier de utils existe ?
        config = ConfigParser.ConfigParser()
        if os.path.isfile(CRConfig.chemin +'centralreport.cfg'):
            print('Fichier de conf : Existant. Lecture.')
        else:
            print('Fichier de conf : Inexistant. Creation.')

            # On ecrit le fichier de conf
            config.add_section('General')
            config.set('General', 'uuid', uuid.uuid1())
            config.add_section('Network')
            config.set('Network', 'enable_check_cpu', True)
            config.set('Network', 'enable_check_memory', True)
            config.set('Network', 'enable_check_loadaverage', True)
            config.set("Network", 'server_addr', 'localhost:8888')
            config.add_section('Webserver')
            config.set("Webserver", 'enable', True)
            config.set("Webserver", 'interface', '0.0.0.0')
            config.set("Webserver", 'port', '8080')


            config.write(open(CRConfig.chemin +'centralreport.cfg','w'))

        # Lecture du fichier de utils
        config.read(CRConfig.chemin +'centralreport.cfg')

        CRConfig.uuid = config.get('General', 'uuid')
        CRConfig.config_enable_check_memory = config.getboolean("Network","enable_check_memory")
        CRConfig.config_enable_check_cpu = config.getboolean("Network","enable_check_cpu")
        CRConfig.config_enable_check_loadaverage = config.getboolean("Network","enable_check_loadaverage")
        CRConfig.config_server_addr = config.get("Network",'server_addr')
        CRConfig.config_webserver_enable = config.getboolean("Webserver","enable")
        CRConfig.config_webserver_interface = config.get("Webserver","interface")
        CRConfig.config_webserver_port = config.getint("Webserver","port")


    @staticmethod
    def determine_current_host():
        """
            Detecting current OS...
        """

        # Est-ce un mac ?
        kernel_mac = subprocess.Popen(['sysctl','-n','kern.ostype'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        kernel_linux = subprocess.Popen(['sysctl','-n','kernel.ostype'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        #print(str(kernel_mac))
        if kernel_mac.startswith("Darwin"):
            # Yes, it's a beautiful Mac !
            CRConfig.HOST_CURRENT = CRConfig.HOST_MAC

        elif kernel_linux.startswith("Linux"):
            # Non ? On est sur linux !
            CRConfig.HOST_CURRENT = CRConfig.HOST_LINUX

            # On va essayer d'affiner en fonction des distributions

            # Utilisation de la liste de Novell pour reconnaitre des distrib Linux
            # http://www.novell.com/coolsolutions/feature/11251.html

            if os.path.isfile("/etc/lsb-release"):
                # Ubuntu !
                CRConfig.HOST_CURRENT = CRConfig.HOST_UBUNTU
            elif os.path.isfile("/etc/debian_version"):
                # Une Debian pure et dure dans ce cas !
                CRConfig.HOST_CURRENT = CRConfig.HOST_DEBIAN
            elif os.path.isfile("/etc/fedora-release"):
                # Fedora !
                CRConfig.HOST_CURRENT = CRConfig.HOST_FEDORA
            elif os.path.isfile("/etc/redhat_version"):
                # RedHat !
                CRConfig.HOST_CURRENT = CRConfig.HOST_REDHAT


        return CRConfig.HOST_CURRENT