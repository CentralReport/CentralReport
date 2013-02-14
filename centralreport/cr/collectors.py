# -*- coding: utf-8 -*-

"""
    CentralReport - Collectors modules
        Contains collectors for Debian/Ubuntu and OS X.

    https://github.com/miniche/CentralReport/
"""

# Summary of this module:
# Collector abstract class
# MacCollector class
# DebianCollector class

import datetime

import multiprocessing
import platform
import socket
import time
from os import getloadavg

import cr.entities.checks as crEntitiesChecks
import cr.entities.host as crEntitiesHost
import cr.log as crLog
import cr.system as crSystem
import cr.utils.text as crUtilsText
from cr.tools import Config


class _Collector:
    def get_infos(self):
        raise NameError('Method not implemented yet')

    def get_cpu(self):
        raise NameError('Method not implemented yet')

    def get_memory(self):
        raise NameError('Method not implemented yet')

    def get_loadaverage(self):
        raise NameError('Method not implemented yet')

    def get_disks(self):
        raise NameError('Method not implemented yet')

    def get_uptime(self):
        raise NameError('Method not implemented yet')


class MacCollector(_Collector):
    """
        Collector executing Mac OS commands and getting useful values.
    """

    PAGEBYTES_TO_BYTES = 4096.
    BLOCKBYTES_TO_BYTES = 512.

    def get_infos(self):
        """
            Gets information about this Mac.
        """

        hostname = crUtilsText.removeSpecialsCharacters(crSystem.executeCommand('hostname -s'))

        architecture = crSystem.executeCommand('sysctl -n hw.machine')

        kernel = crSystem.executeCommand('sysctl -n kern.ostype')
        kernel_v = crSystem.executeCommand('uname -r')

        os_name = crSystem.executeCommand('sw_vers -productName')
        os_version = crSystem.executeCommand('sw_vers -productVersion')

        model = crSystem.executeCommand('sysctl -n hw.model')

        ncpu = crSystem.executeCommand('sysctl -n hw.ncpu')
        cpu_model = crSystem.executeCommand('sysctl -n machdep.cpu.brand_string')

        # Using new HostEntity
        hostEntity = crEntitiesHost.Infos()

        hostEntity.uuid = Config.getConfigValue('General', 'uuid')
        hostEntity.os = Config.HOST_CURRENT
        hostEntity.hostname = hostname
        hostEntity.architecture = architecture
        hostEntity.model = model
        hostEntity.kernelName = kernel
        hostEntity.kernelVersion = kernel_v
        hostEntity.osName = os_name
        hostEntity.osVersion = os_version
        hostEntity.cpuModel = cpu_model
        hostEntity.cpuCount = ncpu

        return hostEntity

    def get_memory(self):
        """
            Gets memory information.
        """

        memory_cmd = crSystem.executeCommand('vm_stat')

        # Each line have a different data
        dict_memory = memory_cmd.splitlines()

        # Formating each line
        for i in range(1, 12):
            dict_memory[i] = dict_memory[i].replace(' ', '')
            dict_memory[i] = dict_memory[i].replace('.', '')
            dict_memory[i] = dict_memory[i].split(':')

        # Getting desired values
        mem_free = (int(dict_memory[1][1]) + int(dict_memory[4][1])) * float(MacCollector.PAGEBYTES_TO_BYTES)
        mem_active = int(dict_memory[2][1]) * float(MacCollector.PAGEBYTES_TO_BYTES)
        mem_inactive = int(dict_memory[3][1]) * float(MacCollector.PAGEBYTES_TO_BYTES)
        mem_resident = int(dict_memory[5][1]) * float(MacCollector.PAGEBYTES_TO_BYTES)
        mem_swap = int(dict_memory[11][1]) * float(MacCollector.PAGEBYTES_TO_BYTES)

        mem_total = (int(dict_memory[1][1]) + int(dict_memory[4][1]) + int(dict_memory[2][1]) + int(dict_memory[3][1])
                     + int(dict_memory[5][1])) * float(MacCollector.PAGEBYTES_TO_BYTES)

        # Preparing return entity...
        memoryCheck = crEntitiesChecks.Memory()
        memoryCheck.total = mem_total
        memoryCheck.free = mem_free
        memoryCheck.active = mem_active
        memoryCheck.inactive = mem_inactive
        memoryCheck.resident = mem_resident
        memoryCheck.swapSize = mem_total
        memoryCheck.swapFree = 0
        memoryCheck.swapUsed = mem_swap

        return memoryCheck

    def get_cpu(self):
        """
            Gets current CPU usage.
        """

        # iostat - entrees / sorties
        iostat = crSystem.executeCommand('iostat -c 2')

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers, values))

        # Use your new CpuCheckEntity!
        cpuCheck = crEntitiesChecks.Cpu()
        cpuCheck.idle = dict_iostat['id']
        cpuCheck.system = dict_iostat['sy']
        cpuCheck.user = dict_iostat['us']

        return cpuCheck

    def get_loadaverage(self):
        """
            Gets the host load average.
        """

        dict_iostat = self.getIOStat()

        # Prepare return entity
        loadAverageEntity = crEntitiesChecks.LoadAverage()
        loadAverageEntity.last1m = dict_iostat['1m']
        loadAverageEntity.last5m = dict_iostat['5m']
        loadAverageEntity.last15m = dict_iostat['15m']

        loadAverageEntity.uptime = self.get_uptime()

        return loadAverageEntity

    def getIOStat(self):
        """
            Gets IOStat dictionary.
        """

        # iostat - entrees / sorties
        iostat = crSystem.executeCommand('iostat -c 2')

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers, values))

        return dict_iostat

    def get_uptime(self):
        """
            Gets the number of seconds since the last boot.
        """
        uptime_cmd = crSystem.executeCommand('sysctl -n kern.boottime')

        # Getting the split dict.
        # The last command return this pattern: { sec = 1353839334, usec = 0 } Sun Nov 25 11:28:54 201)
        # We want to use the first value.
        dict_uptime = uptime_cmd.split(' ')

        try:
            timestamp_boot = int(dict_uptime[3].replace(',', ''))
        except:
            timestamp_boot = time.time()

        return int(time.time()) - int(timestamp_boot)

    def get_disks(self):
        """
            Gets active disks (with disk size for the moment).
        """

        df_dict = crSystem.executeCommand('df')

        df_split = df_dict.splitlines()
        header = df_split[0].split()

        # New return entity
        listDisks = crEntitiesHost.Disks()

        for i in range(1, len(df_split)):
            if df_split[i].startswith('/dev/'):
                line_split = df_split[i].split()
                line_dict = dict(zip(header, line_split))

                # Getting info in MB (Mac OS count with '512 blocks' unit)
                disk_total = int(line_dict['512-blocks']) * MacCollector.BLOCKBYTES_TO_BYTES
                disk_used = int(line_dict['Used']) * MacCollector.BLOCKBYTES_TO_BYTES
                disk_free = int(line_dict['Available']) * MacCollector.BLOCKBYTES_TO_BYTES

                # Getting user friendly name
                disk_name = crSystem.executeCommand('diskutil info "' + line_dict[
                    'Filesystem'] + '" | grep "Volume Name" | awk "BEGIN { FS=\\":\\" } END { print $2; }"')

                # Using new check entity
                checkDisk = crEntitiesChecks.Disk()
                checkDisk.date = datetime.datetime.now()
                checkDisk.name = disk_name.lstrip()
                checkDisk.unix_namename = line_dict['Filesystem']
                checkDisk.size = disk_total
                checkDisk.used = disk_used
                checkDisk.free = disk_free

                listDisks.checks.append(checkDisk)

        return listDisks


class DebianCollector(_Collector):
    """
        Collector executing Debian/Ubuntu commands and getting useful values.
    """

    def get_infos(self):
        """
            Gets information about this host.
        """

        hostname = socket.gethostname()
        kernel = platform.system()
        kernel_v = platform.release()

        # Getting OS Name and OS version
        # Default values
        os_name = 'Linux'
        os_version = ''

        if Config.HOST_DEBIAN == Config.HOST_CURRENT:
            os_name = 'Debian'
            os_version = crSystem.executeCommand('cat /etc/debian_version')

        elif Config.HOST_UBUNTU == Config.HOST_CURRENT:
            os_name = 'Ubuntu'

            # OS version for Ubuntu
            os_version = 'Unknown'
            os_version_full = crSystem.executeCommand('cat /etc/lsb-release')
            os_version_lines = os_version_full.splitlines()

            # Looking for the "DISTRIB_RELEASE" key
            for i in range(0, len(os_version_lines)):
                if os_version_lines[i].startswith('DISTRIB_RELEASE'):
                    try:
                        os_version = os_version_lines[i].split("=")[1].replace(' ', '')
                    except:
                        crLog.writeError('Error getting Ubuntu version')
                        os_version = ''

        hostEntity = crEntitiesHost.Infos()

        # Number of CPU/CPU cores
        try:
            ncpu = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            try:
                ncpu = open('/proc/cpuinfo').read().count('processor\t:')
            except IOError:
                pass

        hostEntity.os = Config.HOST_CURRENT
        hostEntity.hostname = hostname
        hostEntity.cpuCount = ncpu
        hostEntity.kernelName = kernel
        hostEntity.kernelVersion = kernel_v
        hostEntity.osName = os_name
        hostEntity.osVersion = os_version

        return hostEntity

    def get_cpu(self):
        """
            Gets CPU stats.
        """

        # vmstat - input / output
        iostat = crSystem.executeCommand('vmstat 1 2')

        # Formatage de vmstat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers, values))

        # Use your new CpuCheckEntity!
        cpuCheck = crEntitiesChecks.Cpu()
        cpuCheck.idle = dict_iostat['id']
        cpuCheck.system = dict_iostat['sy']
        cpuCheck.user = dict_iostat['us']

        return cpuCheck

    def get_memory(self):
        """
            Gets memory usage.
        """

        memory_result = crSystem.executeCommand('cat /proc/meminfo')

        # On decoupe toutes les lignes
        memory_result_split = memory_result.splitlines()

        # On prepare nos deux listes qui vont servir de modele "cle-valeur"
        list_headers = []
        list_values = []

        # On va parcourir toutes les lignes afin d'obtenir le detail
        for current_line in memory_result_split:
            current_line = current_line.split(':')

            # Suppression des caracteres indesirables
            current_line_values = current_line[1].replace(' ', '')
            current_line_values = current_line_values.replace('kB', '')

            # Ajout dans nos listes
            list_headers.append(current_line[0])
            list_values.append(current_line_values)

        # Creation de notre dictionnaire
        dict_memory = dict(zip(list_headers, list_values))

        # Preparing return entity...
        # Debian return memory sizes in KB.
        memoryCheck = crEntitiesChecks.Memory()
        memoryCheck.total = int(dict_memory['MemTotal']) * 1024
        memoryCheck.free = int(dict_memory['MemFree']) * 1024
        memoryCheck.active = int(dict_memory['Active']) * 1024
        memoryCheck.inactive = int(dict_memory['Inactive']) * 1024
        memoryCheck.resident = 0
        memoryCheck.swapSize = int(dict_memory['SwapTotal']) * 1024
        memoryCheck.swapFree = int(dict_memory['SwapFree']) * 1024
        memoryCheck.swapUsed = int(float(dict_memory['SwapTotal']) - float(dict_memory['SwapFree'])) * 1024

        return memoryCheck

    def get_loadaverage(self):
        """
            Gets load average.
        """

        loadavg_result = getloadavg()

        # On va spliter en fonction des espaces
        dict_loadavg = loadavg_result

        # Prepare return entity
        loadAverageEntity = crEntitiesChecks.LoadAverage()
        loadAverageEntity.last1m = dict_loadavg[0]
        loadAverageEntity.last5m = dict_loadavg[1]
        loadAverageEntity.last15m = dict_loadavg[2]

        loadAverageEntity.uptime = self.get_uptime()

        return loadAverageEntity

    def get_uptime(self):
        """
            Gets the number of seconds since the last boot.
        """
        uptime_cmd = crSystem.executeCommand('cat /proc/uptime')
        uptime_dict = uptime_cmd.split(' ')

        try:
            uptime = int(float(uptime_dict[0]))
        except:
            uptime = int(0)

        return int(uptime)

    def get_disks(self):
        """
            Gets active disks (with disk size for the moment).
        """

        df_dict = crSystem.executeCommand('df')
        df_split = df_dict.splitlines()

        listDisks = crEntitiesHost.Disks()  # Return new entity

        for i in range(1, len(df_split)):
            if df_split[i].startswith('/dev/'):
                line_split = df_split[i].split()

                # Getting info in MB (Linux count with '1K block' unit)
                disk_free = int(line_split[3]) * 1024
                disk_total = int(line_split[1]) * 1024
                disk_used = int(line_split[2]) * 1024

                # Using new check entity
                checkDisk = crEntitiesChecks.Disk()
                checkDisk.date = datetime.datetime.now()
                checkDisk.free = disk_free
                checkDisk.name = line_split[0]
                checkDisk.size = disk_total
                checkDisk.unix_name = line_split[0]
                checkDisk.used = disk_used

                listDisks.checks.append(checkDisk)

        return listDisks
