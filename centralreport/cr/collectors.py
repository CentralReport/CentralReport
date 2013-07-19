# -*- coding: utf-8 -*-

"""
    CentralReport - Collectors modules
        Contains collectors for Debian/Ubuntu and OS X.

    https://github.com/CentralReport
"""

# Summary of this module:
# Collector abstract class
# MacCollector class
# DebianCollector class

import multiprocessing
import platform
import re
import socket
import time
import os

from cr.entities import checks
from cr.entities import host
from cr import system
from cr.utils import text
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

        hostname = text.clean(system.execute_command('hostname -s'))

        architecture = text.clean(platform.machine())

        kernel = text.clean(platform.system())
        kernel_v = text.clean(platform.release())

        os_name = text.clean(system.execute_command('sw_vers -productName'))
        os_version = text.clean(system.execute_command('sw_vers -productVersion'))

        model = text.clean(system.execute_command('sysctl -n hw.model'))

        # Number of CPU/CPU cores
        ncpu = 1

        try:
            ncpu = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            try:
                ncpu = system.execute_command('sysctl -n hw.ncpu')
            except IOError:
                pass

        cpu_model = text.clean(system.execute_command('sysctl -n machdep.cpu.brand_string'))

        # Using new HostEntity
        host_entity = host.Infos()

        host_entity.uuid = Config.get_config_value('General', 'uuid')
        host_entity.key = Config.get_config_value('Online', 'key')
        host_entity.os = Config.HOST_CURRENT
        host_entity.hostname = hostname
        host_entity.architecture = architecture
        host_entity.model = model
        host_entity.kernel_name = kernel
        host_entity.kernel_version = kernel_v
        host_entity.os_name = os_name
        host_entity.os_version = os_version
        host_entity.cpu_model = cpu_model
        host_entity.cpu_count = ncpu

        return host_entity

    def get_cpu(self):
        """
            Gets current CPU usage.
        """

        # iostat - entrees / sorties
        iostat = system.execute_command('iostat -c 2')

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers, values))

        # Use your new CpuCheckEntity!
        cpu_check = checks.Cpu()
        cpu_check.idle = dict_iostat['id']
        cpu_check.system = dict_iostat['sy']
        cpu_check.user = dict_iostat['us']

        return cpu_check

    def get_memory(self):
        """
            Gets memory information.
        """

        memory_cmd = system.execute_command('vm_stat')

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
        memory_check = checks.Memory()
        memory_check.total = mem_total
        memory_check.free = mem_free
        memory_check.active = mem_active
        memory_check.inactive = mem_inactive
        memory_check.resident = mem_resident
        memory_check.swap_size = mem_total
        memory_check.swap_free = 0
        memory_check.swap_used = mem_swap

        return memory_check

    def get_loadaverage(self):
        """
            Gets load average.
        """

        # On va spliter en fonction des espaces
        dict_loadavg = os.getloadavg()

        # Prepare return entity
        load_average_entity = checks.LoadAverage()
        # Split after 2 decimals
        load_average_entity.last1m = "%.2f" % dict_loadavg[0]
        load_average_entity.last5m = "%.2f" % dict_loadavg[1]
        load_average_entity.last15m = "%.2f" % dict_loadavg[2]

        load_average_entity.uptime = self.get_uptime()

        return load_average_entity

    def get_uptime(self):
        """
            Gets the number of seconds since the last boot.
        """
        uptime_cmd = system.execute_command('sysctl -n kern.boottime')

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

        df_dict = system.execute_command('df')

        df_split = df_dict.splitlines()
        header = df_split[0].split()

        # New return entity
        list_disks = checks.Disks()

        for i in range(1, len(df_split)):
            if df_split[i].startswith('/dev/'):
                line_split = df_split[i].split()
                line_dict = dict(zip(header, line_split))

                # Getting info in MB (Mac OS count with '512 blocks' unit)
                disk_total = int(line_dict['512-blocks']) * MacCollector.BLOCKBYTES_TO_BYTES
                disk_used = int(line_dict['Used']) * MacCollector.BLOCKBYTES_TO_BYTES
                disk_free = int(line_dict['Available']) * MacCollector.BLOCKBYTES_TO_BYTES

                # Getting user friendly name
                disk_name = system.execute_command('diskutil info "' + line_dict['Filesystem'] + '"'
                                                   ' | grep "Volume Name"'
                                                   ' | awk "BEGIN { FS=\\":\\" } END { print $2; }"')

                disk_uuid = system.execute_command('diskutil info "' + line_dict['Filesystem'] + '"'
                                                   ' | grep "Volume UUID"'
                                                   ' | awk "BEGIN { FS=\\":\\" } END { print $2; }"')

                # Using new check entity
                check_disk = checks.Disk()
                check_disk.name = text.clean(line_dict['Filesystem'])
                check_disk.display_name = text.clean(disk_name.lstrip())
                check_disk.uuid = disk_uuid
                check_disk.size = disk_total
                check_disk.used = disk_used
                check_disk.free = disk_free

                list_disks.disks.append(check_disk)

        return list_disks


class DebianCollector(_Collector):
    """
        Collector executing Debian/Ubuntu commands and getting useful values.
    """

    def get_infos(self):
        """
            Gets information about this host.
        """

        hostname = text.clean(socket.gethostname())
        architecture = text.clean(platform.machine())

        kernel = text.clean(platform.system())
        kernel_v = text.clean(platform.release())

        # Getting OS Name and OS version
        from platform import linux_distribution as dist

            # Getting OS Name and OS version
        try:
            os_name = text.clean(dist()[0])
            os_version = dist()[1]
        except:
            os_name = 'Linux'
            os_version = ''

        # TODO Find a way to find the computer model
        #model = system.execute_command('sysctl -n hw.model')

        # Number of CPU/CPU cores
        ncpu = 1

        try:
            ncpu = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            try:
                ncpu = open('/proc/cpuinfo').read().count('processor\t:')
            except IOError:
                pass

        cpu_infos = system.execute_command('cat /proc/cpuinfo | grep "model name"')
        if "model name" in cpu_infos:
            cpu_model = text.clean(re.sub(".*model name.*:", "", cpu_infos, 1))
        else:
            cpu_model = 'CPU model unknown'

        # Using new HostEntity
        host_entity = host.Infos()

        host_entity.uuid = Config.get_config_value('General', 'uuid')
        host_entity.key = Config.get_config_value('Online', 'key')
        host_entity.os = Config.HOST_CURRENT
        host_entity.hostname = hostname
        host_entity.architecture = architecture
        #host_entity.model = model
        host_entity.kernel_name = kernel
        host_entity.kernel_version = kernel_v
        host_entity.os_name = os_name
        host_entity.os_version = os_version
        host_entity.cpu_model = cpu_model
        host_entity.cpu_count = ncpu

        return host_entity

    def get_cpu(self):
        """
            Gets CPU stats.
        """

        # vmstat - input / output
        iostat = system.execute_command('vmstat 1 2')

        # Formatage de vmstat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers, values))

        # Use your new CpuCheckEntity!
        cpu_check = checks.Cpu()
        cpu_check.idle = dict_iostat['id']
        cpu_check.system = dict_iostat['sy']
        cpu_check.user = dict_iostat['us']

        return cpu_check

    def get_memory(self):
        """
            Gets memory usage.
        """

        memory_result = system.execute_command('cat /proc/meminfo')

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
        memory_check = checks.Memory()
        memory_check.total = int(dict_memory['MemTotal']) * 1024
        memory_check.free = int(dict_memory['MemFree']) * 1024
        memory_check.active = int(dict_memory['Active']) * 1024
        memory_check.inactive = int(dict_memory['Inactive']) * 1024
        memory_check.resident = 0
        memory_check.swap_size = int(dict_memory['SwapTotal']) * 1024
        memory_check.swap_free = int(dict_memory['SwapFree']) * 1024
        memory_check.swap_used = int(float(dict_memory['SwapTotal']) - float(dict_memory['SwapFree'])) * 1024

        return memory_check

    def get_loadaverage(self):
        """
            Gets load average.
        """

        loadavg_result = os.getloadavg()

        # On va spliter en fonction des espaces
        dict_loadavg = loadavg_result

        # Prepare return entity
        load_average_entity = checks.LoadAverage()
        load_average_entity.last1m = dict_loadavg[0]
        load_average_entity.last5m = dict_loadavg[1]
        load_average_entity.last15m = dict_loadavg[2]

        load_average_entity.uptime = self.get_uptime()

        return load_average_entity

    def get_uptime(self):
        """
            Gets the number of seconds since the last boot.
        """
        uptime_cmd = system.execute_command('cat /proc/uptime')
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

        # Getting all disks by UUID
        disks_by_uuid = {}
        list_disks_uuid = os.listdir('/dev/disk/by-uuid/')

        # This associates UUID with the partition name
        for disk in list_disks_uuid:
            disks_by_uuid[disk] = os.path.realpath(os.path.join('/dev/disk/by-uuid/', disk))

        # The "df" command is used to get the size of each disk
        df_dict = system.execute_command('df -kP')
        df_split = df_dict.splitlines()

        list_disks = checks.Disks()

        for i in range(1, len(df_split)):
            if df_split[i].startswith('/dev/'):
                line_split = df_split[i].split()

                # On Linux, "df" can return two name possibilities:
                # - /dev/disk/by-uuid/(uuid)
                # - /dev/(partition_name)
                # We keep only the last part
                disk_id_dict = line_split[0].split('/')
                disk_id = disk_id_dict[-1]

                # Default values whenever the disk_id is not found in the uuid dictionary.
                disk_name = disk_id
                disk_uuid = ''

                if disk_id in disks_by_uuid:
                    disk_name = disks_by_uuid[disk_id]
                    disk_uuid = disk_id
                else:
                    for key, value in disks_by_uuid:
                        if value == disk_id:
                            disk_name = value
                            disk_uuid = key

                check_disk = checks.Disk()
                check_disk.name = text.clean(disk_name)
                check_disk.display_name = text.clean(disk_name.replace('/dev/', ''))
                check_disk.uuid = disk_uuid

                # Linux count with '1K block' unit
                check_disk.size = int(line_split[1]) * 1024
                check_disk.used = int(line_split[2]) * 1024
                check_disk.free = int(line_split[3]) * 1024

                list_disks.disks.append(check_disk)

        return list_disks
