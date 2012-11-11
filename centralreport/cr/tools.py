#
# CentralReport - Indev version
#

# This module contains the config class

import ConfigParser, os, uuid, subprocess,getpass

class Config:

    config = ConfigParser.ConfigParser()

    # CentralReport Core config
    if getpass.getuser() != "root":
        pid_file = "/tmp/centralreport.pid"
    else:
        pid_file = "/var/run/centralreport.pid"

    # Indev config
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
        Config.determine_current_host()

        if Config.HOST_CURRENT == Config.HOST_MAC:
            # On est sur Mac. Test du repertoire
            if os.path.isdir("/etc/cr") != True:
                # Creation du dossier
                os.mkdir("/etc/cr")

            Config.chemin = "/etc/cr/"
            print("Mac config")
        else:
            # On est sur un systeme Linux

            if os.path.isdir("/etc/cr") != True:
                # Creation du dossier
                os.mkdir("/etc/cr")
            Config.chemin = "/etc/cr/"
            print("Linux config")


        # Fichier de utils existe ?
        config = ConfigParser.ConfigParser()
        if os.path.isfile(Config.chemin +'centralreport.cfg'):
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


            config.write(open(Config.chemin +'centralreport.cfg','w'))

        # Lecture du fichier de utils
        config.read(Config.chemin +'centralreport.cfg')

        Config.uuid = config.get('General', 'uuid')
        Config.config_enable_check_memory = config.getboolean("Network","enable_check_memory")
        Config.config_enable_check_cpu = config.getboolean("Network","enable_check_cpu")
        Config.config_enable_check_loadaverage = config.getboolean("Network","enable_check_loadaverage")
        Config.config_server_addr = config.get("Network",'server_addr')
        Config.config_webserver_enable = config.getboolean("Webserver","enable")
        Config.config_webserver_interface = config.get("Webserver","interface")
        Config.config_webserver_port = config.getint("Webserver","port")


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
            Config.HOST_CURRENT = Config.HOST_MAC

        elif kernel_linux.startswith("Linux"):
            # Non ? On est sur linux !
            Config.HOST_CURRENT = Config.HOST_LINUX

            # On va essayer d'affiner en fonction des distributions

            # Utilisation de la liste de Novell pour reconnaitre des distrib Linux
            # http://www.novell.com/coolsolutions/feature/11251.html

            if os.path.isfile("/etc/lsb-release"):
                # Ubuntu !
                Config.HOST_CURRENT = Config.HOST_UBUNTU
            elif os.path.isfile("/etc/debian_version"):
                # Une Debian pure et dure dans ce cas !
                Config.HOST_CURRENT = Config.HOST_DEBIAN
            elif os.path.isfile("/etc/fedora-release"):
                # Fedora !
                Config.HOST_CURRENT = Config.HOST_FEDORA
            elif os.path.isfile("/etc/redhat_version"):
                # RedHat !
                Config.HOST_CURRENT = Config.HOST_REDHAT


