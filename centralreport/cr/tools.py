# -*- coding: utf-8 -*-

"""
    CentralReport - Tools module
        Contrains Config class

    https://github.com/miniche/CentralReport/
"""

import ConfigParser
import os
import platform

import uuid

from cr import log


class Config:
    """
        Manages CentralReport configuration.
    """

    # Python object used to manage the config file.
    config = ConfigParser.ConfigParser()
    CR_VERSION_MAJOR = 0
    CR_VERSION_MINOR = 1
    CR_VERSION_REVISION = 0
    CR_VERSION = '%s.%s.%s' % (CR_VERSION_MAJOR, CR_VERSION_MINOR, CR_VERSION_REVISION)
    CR_VERSION_NAME = 'Alpha Version'
    CR_CONFIG_PATH = '/etc/centralreport'  # Config file location
    CR_CONFIG_FILE = 'centralreport.cfg'
    CR_CONFIG_FULL_PATH = os.path.join(CR_CONFIG_PATH, CR_CONFIG_FILE)
    CR_CONFIG_ENABLE_DEBUG_MODE = False  # False = Production environment. True = debug/test/develop environment.

    # Default interval between two checks (use this if not available in the config file)
    CR_CONFIG_DEFAULT_CHECKS_INTERVAL = int(60)

    # Current host
    HOST_CURRENT = ''

    # Some hosts...
    HOST_MAC = 'Mac OS X'
    HOST_LINUX = 'Linux'
    HOST_DEBIAN = 'Debian'
    HOST_UBUNTU = 'Ubuntu'
    HOST_REDHAT = 'RedHat'
    HOST_FEDORA = 'Fedora'

    # CentralReport pid file
    if CR_CONFIG_ENABLE_DEBUG_MODE:
        CR_PID_FILE = '/tmp/centralreport.pid'

    else:
        CR_PID_FILE = '/var/run/centralreport/centralreport.pid'

    # Customizable values. This values are stored in the config file.
    # Values are default values and can by updated by config file content.
    # Please only use string values, and cast it in your code.

    _CR_CONFIG_VALUES = {
        'General': {
            'uuid': ''
        },
        'Webserver': {
            'enable': 'True',
            'interface': '0.0.0.0',
            'port': '8080'
        },
        'Checks': {
            'enable_cpu_check': 'True',
            'enable_memory_check': 'True',
            'enable_load_check': 'True',
            'enable_disks_check': 'True',
            'interval': '60'
        },
        'Alerts': {
            'cpu_warning': '75',
            'cpu_alert': '90',
            'memory_warning': '75',
            'memory_alert': '90',
            'swap_warning': '1',
            'swap_alert': '75',
            'load_warning': '75',
            'load_alert': '90'
        },
    }

    def __init__(self):
        """
            Constructor
        """

        Config.determine_current_host()

        if Config.HOST_CURRENT == Config.HOST_MAC:
            log.log_debug('Mac config')
        else:
            log.log_debug('Linux config')

        # Managing config file
        if os.path.isfile(Config.CR_CONFIG_FULL_PATH):
            log.log_debug('Configuration file: Found. Reading it.')
            self.read_config_file()
        else:
            log.log_info('Configuration file: Not found. Creating it.')
            self.write_config_file()

    def read_config_file(self):
        """
            Reads the configuration file.
        """

        log.log_debug('Reading the config file...')

        # Using Python ConfigParser module to read the file
        Config.config.read(Config.CR_CONFIG_FULL_PATH)

        # False = all sections and options are found.
        # True = config must be updated: some options or sections are mising (outdated config file?)
        config_must_be_updated = False

        # Getting all values...
        for config_section in Config._CR_CONFIG_VALUES:
            for config_value in Config._CR_CONFIG_VALUES[config_section]:
                try:
                    Config._CR_CONFIG_VALUES[config_section][config_value] = \
                        Config.config.get(config_section, config_value)

                except ConfigParser.NoSectionError:
                    config_must_be_updated = True
                    log.log_error('Config section does not exist in the file: %s' % config_section)

                except ConfigParser.NoOptionError:
                    config_must_be_updated = True
                    log.log_error('Config value does not exist in the file: %s' % config_value)

                except:
                    config_must_be_updated = True
                    log.log_error('Error getting a config value: %s/%s' % (config_section, config_value))

        # In this case, config file have been written by a last version of CR.
        # We must update it to include new sections or options.
        if config_must_be_updated:
            self.write_config_file()

    def write_config_file(self):
        """
            Writes the actual configuration into the config file.
        """

        log.log_info('Writing the config file...')

        # Generating uuid if empty
        if '' == Config.get_config_value('General', 'uuid'):
            Config.set_config_value('General', 'uuid', uuid.uuid1())

        # Writing conf file. Reading all sections defined in the config...
        for config_section in Config._CR_CONFIG_VALUES:
            try:
                Config.config.add_section(config_section)
            except ConfigParser.DuplicateSectionError:
                log.log_debug('Section already exist: %s' % config_section)
            except:
                log.log_error('Error creating new section: %s:%s' % (config_section, Exception.message))

            # Reading all values in this section
            config_section_vars = Config._CR_CONFIG_VALUES[config_section]

            for config_value in config_section_vars:
                try:
                    Config.config.set(config_section, config_value, Config._CR_CONFIG_VALUES[config_section][config_value])
                except:
                    log.log_error('Error writing config value: %s/%s' % (config_section, config_value))

        try:
            Config.config.write(open(Config.CR_CONFIG_FULL_PATH, 'w'))  # Writing the config file on filesystem...

        except IOError:
            log.log_error('/!\ Error writing config file. Using the default config')

    @staticmethod
    def get_config_value(section, variable):
        """
            Gets a config value.
        """

        try:
            return Config._CR_CONFIG_VALUES[section][variable]
        except:
            raise NameError('Section or Variable not found! (%s/%s)' % (section, variable))

    @staticmethod
    def set_config_value(section, variable, value):
        """
            Adds a new value to a config variable, in a defined section
        """

        try:
            Config._CR_CONFIG_VALUES[section][variable] = value
        except:
            raise NameError('Section or Variable not found! (%s/%s)' % (section, variable))

    @staticmethod
    def determine_current_host():
        """
            Detecting current OS...
        """

        kernel = platform.system()

        if kernel.startswith('Darwin'):
            Config.HOST_CURRENT = Config.HOST_MAC
        elif kernel.startswith('Linux'):
            Config.HOST_CURRENT = Config.HOST_LINUX

            # On va essayer d'affiner en fonction des distributions

            # Utilisation de la liste de Novell pour reconnaitre des distrib Linux
            # http://www.novell.com/coolsolutions/feature/11251.html

            if os.path.isfile('/etc/lsb-release'):
                # Ubuntu!
                Config.HOST_CURRENT = Config.HOST_UBUNTU
            elif os.path.isfile('/etc/debian_version'):
                # Une Debian pure et dure dans ce cas!
                Config.HOST_CURRENT = Config.HOST_DEBIAN
            elif os.path.isfile('/etc/fedora-release'):
                # Fedora!
                Config.HOST_CURRENT = Config.HOST_FEDORA
            elif os.path.isfile('/etc/redhat_version'):
                # RedHat!
                Config.HOST_CURRENT = Config.HOST_REDHAT
