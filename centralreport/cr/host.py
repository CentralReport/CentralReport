# -*- coding: utf-8 -*-

"""
    CentralReport - Collectors modules
        Contains collectors for Debian/Ubuntu and OS X.

    https://github.com/CentralReport
"""

import platform
import multiprocessing
import re
import socket

import cr.entities.host as crEntityHost
import cr.utils.text as text
import system

#: @type _current_host: cr.entities.host.Host
_current_host = None

# OS family names
FAMILY_UNIX = 'Unix'
FAMILY_LINUX = 'Linux'
FAMILY_UNKNOWN = 'Unknown'

# Family variant
VARIANT_MAC = 'Mac'
VARIANT_DEBIAN = 'Debian'
VARIANT_REDHAT = 'RedHat'
VARIANT_UNKNOWN = 'Unknown'

# Specific OS names
OS_MAC = 'OS X'
OS_DEBIAN = 'Debian'
OS_UBUNTU = 'Ubuntu'
OS_CENTOS = 'CentOS'
OS_UNKNOWN = 'Unsupported'


def get_current_host():
    """
        Gets the Host object, for the current OS

        @return: cr.entities.host.Host
    """

    global _current_host

    if _current_host is not None:
        return _current_host

    _current_host = crEntityHost.Host()

    _current_host.family = FAMILY_UNKNOWN
    _current_host.variant = VARIANT_UNKNOWN
    _current_host.os = OS_UNKNOWN

    kernel = platform.system()

    if kernel.startswith('Darwin'):
        _current_host.family = FAMILY_UNIX
        _current_host.variant = VARIANT_MAC
        _current_host.os = OS_MAC

    elif kernel.startswith('Linux'):
        _current_host.family = FAMILY_LINUX

        if platform.linux_distribution()[0] == "Ubuntu":
            _current_host.variant = VARIANT_DEBIAN
            _current_host.os = OS_UBUNTU

        elif platform.linux_distribution()[0] == "debian":
            _current_host.variant = VARIANT_DEBIAN
            _current_host.os = OS_DEBIAN

        elif platform.linux_distribution()[0] == "CentOS":
            _current_host.variant = VARIANT_REDHAT
            _current_host.os = OS_CENTOS

        else:
            return _current_host

    else:
        return _current_host

    # Common getters between all OS families
    _current_host.architecture = platform.machine()
    _current_host.kernel_name = kernel
    _current_host.kernel_version = platform.release()

    # Specific getters
    if _current_host.os == OS_MAC:
        _current_host.hostname = text.remove_specials_characters(system.execute_command('hostname -s'))
        _current_host.os_name = system.execute_command('sw_vers -productName')
        _current_host.os_version = text.remove_specials_characters(system.execute_command('sw_vers -productVersion'))
        _current_host.model = system.execute_command('sysctl -n hw.model')

        _current_host.cpu_model = system.execute_command('sysctl -n machdep.cpu.brand_string')
        _current_host.cpu_count = 1
        try:
            _current_host.cpu_count = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            try:
                _current_host.cpu_count = system.execute_command('sysctl -n hw.ncpu')
            except IOError:
                pass

    if _current_host.family == FAMILY_LINUX:
        _current_host.hostname = socket.gethostname()
        _current_host.os_name = platform.linux_distribution()[0]
        _current_host.os_version = platform.linux_distribution()[1]

        _current_host.cpu_count = 1
        try:
            _current_host.cpu_count = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            try:
                _current_host.cpu_count = open('/proc/cpuinfo').read().count('processor\t:')
            except IOError:
                pass

        cpu_info = system.execute_command('cat /proc/cpuinfo | grep "model name"')
        if "model name" in cpu_info:
            _current_host.cpu_model = re.sub(".*model name.*:", "", cpu_info, 1)
        else:
            _current_host.cpu_model = 'CPU model unknown'
