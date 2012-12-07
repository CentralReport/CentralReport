#
# CentralReport - Indev version
#

# This module contains the config class

import ConfigParser
import os
import uuid
import subprocess
import log as crLog


class Config:
    """
        Manage CentralReport config vars.
    """

    # Python object used to manage the config file.
    config = ConfigParser.ConfigParser()

    # Constants : Config file location
    CR_CONFIG_PATH = '/etc'
    CR_CONFIG_FILE = 'centralreport.cfg'
    CR_CONFIG_FULL_PATH = os.path.join(CR_CONFIG_PATH,CR_CONFIG_FILE)

    # Debug mode
    # False = Production environment. True = debug/test/develop environment.
    CR_CONFIG_ENABLE_DEBUG_MODE = False

    # Current host
    HOST_CURRENT = ''
    # Some hosts...
    HOST_MAC = 'Mac OS X'
    HOST_LINUX = 'Linux'
    HOST_DEBIAN = 'Debian'
    HOST_UBUNTU = 'Ubuntu'
    HOST_REDHAT = 'RedHat'
    HOST_FEDORA = 'Fedora'


    # Universal Unique IDentifier for the current host. '' = not defined yet.
    CR_HOST_UUID = ''

    # CentralReport pid file
    if True == CR_CONFIG_ENABLE_DEBUG_MODE:
        CR_PID_FILE = '/tmp/centralreport.pid'
    else:
        CR_PID_FILE = '/var/run/centralreport.pid'


    # Customizable values. This values are stored in the config file.
    # Values are default values and can by updated by config file content.
    _CR_CONFIG_VALUES = {
        'General':
            {
                'uuid':''
            },
        'Webserver':
            {
                'enable':True,
                'interface':'0.0.0.0',
                'port':'8080'
            },
        'Checks':
            {
                'enable_cpu_check':True,
                'enable_memory_check':True,
                'enable_load_check':True,
                'enable_disks_check':True
            }
    }


    # Indev config - Not used for the moment
    #config_enable_check_memory = True
    #config_enable_check_cpu = True
    #config_enable_check_loadaverage = True
    #config_server_addr = ''

    # CherryPy webserver config
    #config_webserver_enable = True
    #config_webserver_interface = '0.0.0.0'
    #config_webserver_port = 8080


    def __init__(self):
        """
            Constructor
        """

        # Determining current host/os
        Config.determine_current_host()

        if Config.HOST_CURRENT == Config.HOST_MAC:
            crLog.writeDebug('Mac config')
        else:
            crLog.writeDebug('Linux config')

        # miniche 22/11/2012 : /etc/ must already exist.
        # Creating the dir if it does not exists
        #if not os.path.isdir(self.CR_CONFIG_PATH):
        #    os.mkdir(self.CR_SYSTEM_PATH)
        #Config.chemin = self.CR_SYSTEM_PATH + '/'

        # Managing config file
        if os.path.isfile(Config.CR_CONFIG_FULL_PATH):
            crLog.writeDebug('Configuration file : Found. Reading it.')
            self.readConfigFile()
        else:
            crLog.writeInfo('Configuration file : Not found. Creating it.')
            self.writeConfigFile()

        # Utils file



    def readConfigFile(self):
        """ Read config file """

        crLog.writeDebug('Reading the config file...')

        # Using Python ConfigParser module to read the file
        Config.config.read(Config.CR_CONFIG_FULL_PATH)

        # False = all sections and options are found.
        # True = config must be updated : some options or sections are mising (outdated config file ?)
        config_must_be_updated = False

        # Getting all values...
        for config_section in Config._CR_CONFIG_VALUES:

            for config_value in Config._CR_CONFIG_VALUES[config_section]:

                try:
                    Config._CR_CONFIG_VALUES[config_section][config_value] = Config.config.get(config_section,config_value)
                except ConfigParser.NoSectionError:
                    config_must_be_updated = True
                    crLog.writeError('Config section not exist in the file : '+ config_section)
                except ConfigParser.NoOptionError:
                    config_must_be_updated = True
                    crLog.writeError('Config value not exist in the file : '+ config_value)
                except:
                    config_must_be_updated = True
                    crLog.writeError('Error getting a config value : '+ config_section +'/'+ config_value)


        # In this case, config file have been written by a last version of CR. We must update it to include new sections or options.
        if True == config_must_be_updated:
            self.writeConfigFile()



    def writeConfigFile(self):
        """  Write into the config file the actual configuration. """

        crLog.writeInfo('Writing the config file...')

        # Generating uuid if empty
        if '' == Config.CR_HOST_UUID:
            Config.CR_HOST_UUID = uuid.uuid1()

        # Writing conf file. Reading all sections defined in the config...
        for config_section in Config._CR_CONFIG_VALUES:

            try:
                Config.config.add_section(config_section)
            except ConfigParser.DuplicateSectionError:
                crLog.writeDebug('Section already exist : '+ config_section)
            except:
                crLog.writeError('Error creating new section : '+ config_section +' : '+ Exception.message)

            # Reading all values in this section
            config_section_vars = Config._CR_CONFIG_VALUES[config_section]
            for config_value in config_section_vars:

                try:
                    Config.config.set(config_section,config_value,Config._CR_CONFIG_VALUES[config_section][config_value])
                except:
                    crLog.writeError('Error writing config value : '+ config_section +'/'+ config_value)


        # Writing the config file on filesystem...
        try:
            Config.config.write(open(Config.CR_CONFIG_FULL_PATH, 'w'))
        except IOError:
            crLog.writeError('/!\ Error writing config file. Using the default config')


    @staticmethod
    def getConfigValue(section,variable):
        """
            Getting a config value
        """
        try:
            return Config._CR_CONFIG_VALUES[section][variable]
        except:
            raise NameError('Section or Variable not found ! ('+ section +'/'+ variable +')')


    @staticmethod
    def setConfigValue(section,variable,value):
        """
            Setting new value to a config variable, in a defined section
        """

        try:
            Config._CR_CONFIG_VALUES[section][variable] = value
        except:
            raise NameError('Section or Variable not found ! ('+ section +'/'+ variable +')')


    @staticmethod
    def determine_current_host():
        """
            Detecting current OS...
        """

        try:
            kernel_mac = subprocess.Popen(
                ['sysctl', '-n', 'kern.ostype'],
                stdout=subprocess.PIPE,
                close_fds=True
            ).communicate()[0]
        except:
            kernel_linux = subprocess.Popen(
                ['sysctl', '-n', 'kernel.ostype'],
                stdout=subprocess.PIPE,
                close_fds=True
            ).communicate()[0]

        if kernel_mac.startswith('Darwin'):
            Config.HOST_CURRENT = Config.HOST_MAC
        elif kernel_linux.startswith('Linux'):
            Config.HOST_CURRENT = Config.HOST_LINUX

            # On va essayer d'affiner en fonction des distributions

            # Utilisation de la liste de Novell pour reconnaitre des distrib Linux
            # http://www.novell.com/coolsolutions/feature/11251.html

            if os.path.isfile('/etc/lsb-release'):
                # Ubuntu !
                Config.HOST_CURRENT = Config.HOST_UBUNTU
            elif os.path.isfile('/etc/debian_version'):
                # Une Debian pure et dure dans ce cas !
                Config.HOST_CURRENT = Config.HOST_DEBIAN
            elif os.path.isfile('/etc/fedora-release'):
                # Fedora !
                Config.HOST_CURRENT = Config.HOST_FEDORA
            elif os.path.isfile('/etc/redhat_version'):
                # RedHat !
                Config.HOST_CURRENT = Config.HOST_REDHAT
