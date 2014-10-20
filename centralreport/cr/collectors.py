# -*- coding: utf-8 -*-

"""
    CentralReport - Collectors modules
        Contains collectors for Debian/Ubuntu and OS X.

    https://github.com/CentralReport
"""

import datetime
from distutils import version
import time
import os

from cr import system
import cr.host
from cr.entities import checks
from cr.entities import host
from cr.utils import text


class _Collector:
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

    def get_cpu(self):
        """
            Gets current CPU usage.
        """

        # https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/iostat.8.html
        iostat = system.execute_command('iostat -c 2')

        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()
        dict_iostat = dict(zip(headers, values))

        cpu_check = checks.Cpu()
        cpu_check.idle = dict_iostat['id']
        cpu_check.system = dict_iostat['sy']
        cpu_check.user = dict_iostat['us']

        return cpu_check

    def get_memory(self):
        """
            Gets memory information.
        """

        # https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/vm_stat.1.html
        memory_cmd = system.execute_command('vm_stat')

        dict_wm_stat = memory_cmd.splitlines()
        dict_memory = dict()

        for i in range(1, len(dict_wm_stat)):
            dict_wm_stat[i] = dict_wm_stat[i].split(':')
            dict_wm_stat[i][1] = dict_wm_stat[i][1].replace(' ', '')
            dict_wm_stat[i][1] = dict_wm_stat[i][1].replace('.', '')
            dict_memory[str(dict_wm_stat[i][0])] = dict_wm_stat[i][1]

        # Getting desired values
        mem_free = (int(dict_memory['Pages free']) + int(dict_memory['Pages speculative']))
        mem_active = int(dict_memory['Pages active'])
        mem_resident = int(dict_memory['Pages wired down'])

        if version.StrictVersion(cr.host.get_current_host().os_version) < version.StrictVersion('10.9.0'):
            mem_inactive = int(dict_memory['Pages inactive'])
            mem_swap = int(dict_memory['Pageouts'])
        else:
            # On 10.9 and newer, Apple uses the WKdm algorithm.
            # More details here: http://terpconnect.umd.edu/~barua/matt-compress-tr.pdf
            mem_inactive = int(dict_memory['Pages inactive']) + int(dict_memory['Pages occupied by compressor'])
            pages_swap_out = int(dict_memory['Swapouts']) - int(dict_memory['Swapins'])
            mem_swap = 0 if pages_swap_out < 0 else pages_swap_out

        mem_total = mem_free + mem_active + mem_inactive + mem_resident

        memory_check = checks.Memory()
        memory_check.total = int(mem_total * float(MacCollector.PAGEBYTES_TO_BYTES))
        memory_check.free = int(mem_free * float(MacCollector.PAGEBYTES_TO_BYTES))
        memory_check.active = int(mem_active * float(MacCollector.PAGEBYTES_TO_BYTES))
        memory_check.inactive = int(mem_inactive * float(MacCollector.PAGEBYTES_TO_BYTES))
        memory_check.resident = int(mem_resident * float(MacCollector.PAGEBYTES_TO_BYTES))
        memory_check.swap_size = int(mem_total * float(MacCollector.PAGEBYTES_TO_BYTES))
        memory_check.swap_free = 0
        memory_check.swap_used = int(mem_swap * float(MacCollector.PAGEBYTES_TO_BYTES))

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
                check_disk.uuid = text.clean(disk_uuid)
                check_disk.size = disk_total
                check_disk.used = disk_used
                check_disk.free = disk_free

                list_disks.disks.append(check_disk)

        return list_disks


class DebianCollector(_Collector):
    """
        Collector executing Debian/Ubuntu commands and getting useful values.
    """

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

        if os.path.isdir('/dev/disk/by-uuid/'):
            return self._get_disks_by_uuid()
        else:
            return self._get_disks_without_uuid()

    def _get_disks_without_uuid(self):
        """
            Gets all disks by querying "df" command (does not handles Disks UUID)
            Use only this method when the /dev/disk/by-uuid/ folder is not available (like in OpenVZ virtual machine)
        """

        df_dict = system.execute_command('df -kP')
        df_split = df_dict.splitlines()

        list_disks = checks.Disks()

        for i in range(1, len(df_split)):
            if df_split[i].startswith('/dev/'):
                line_split = df_split[i].split()

                disk_dict = line_split[0].split('/')
                disk_name = disk_dict[-1]

                check_disk = checks.Disk()
                check_disk.name = text.clean(disk_name)
                check_disk.display_name = text.clean(disk_name.replace('/dev/', ''))
                check_disk.uuid = disk_name

                # Linux count with '1K block' unit
                check_disk.size = int(line_split[1]) * 1024
                check_disk.used = int(line_split[2]) * 1024
                check_disk.free = int(line_split[3]) * 1024

                list_disks.disks.append(check_disk)

        return list_disks

    def _get_disks_by_uuid(self):
        """
            Gets all active disks by UUID
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
                    for key, value in disks_by_uuid.iteritems():
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
