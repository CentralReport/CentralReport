#
# CentralReport - Indev version
#

# Summary of this module :
# Collector abstract class
# MacCollector class
# DebianCollector class

import subprocess
import datetime
import time
import cr.utils.text as crUtilsText
import cr.entities.checks as crEntitiesChecks
import cr.entities.host as crEntitiesHost
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


class MacCollector(_Collector):
    """
        This collector can execute Mac OS command and get some useful values.
    """

    PAGEBYTES_TO_MBYTES = 4096./ 1024./1024.
    BLOCKBYTES_TO_MBYTES = 512./1024./1024.

    def get_infos(self):
        """
            Getting some informations on this Mac.
        """

        subprocessPIPE = subprocess.PIPE
        hostname = crUtilsText.removeSpecialsCharacters(subprocess.Popen(['hostname', '-s'], stdout=subprocessPIPE, close_fds=True).communicate()[0])

        uname = subprocess.Popen(['uname', '-a'], stdout=subprocessPIPE, close_fds=True).communicate()[0]

        kernel = subprocess.Popen(['sysctl', '-n', 'kern.ostype'], stdout=subprocessPIPE, close_fds=True).communicate()[0]
        kernel_v = subprocess.Popen(['uname', '-r'], stdout=subprocessPIPE, close_fds=True).communicate()[0]
        model = subprocess.Popen(['sysctl', '-n', 'hw.model'], stdout=subprocessPIPE, close_fds=True).communicate()[0]
        ncpu = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'], stdout=subprocessPIPE, close_fds=True).communicate()[0]
        memsize = subprocess.Popen(['sysctl', '-n', 'hw.memsize'], stdout=subprocessPIPE, close_fds=True).communicate()[0]
        architecture = subprocess.Popen(['sysctl', '-n', 'hw.machine'], stdout=subprocessPIPE, close_fds=True).communicate()[0]

        cpu_model = subprocess.Popen(['sysctl', '-n', 'machdep.cpu.brand_string'], stdout=subprocessPIPE, close_fds=True).communicate()[0]

        # Using new HostEntity
        hostEntity = crEntitiesHost.Infos()

        hostEntity.uuid = Config.uuid

        hostEntity.os = Config.HOST_CURRENT
        hostEntity.hostname = hostname
        hostEntity.architecture = architecture

        hostEntity.model = model

        hostEntity.kernelName = kernel
        hostEntity.kernelVersion = kernel_v

        hostEntity.cpuModel = cpu_model
        hostEntity.cpuCount = ncpu

        return hostEntity

    def get_memory(self):
        """
            Getting memory informations.
        """

        subprocessPIPE = subprocess.PIPE
        memsize = subprocess.Popen(['sysctl', '-n', 'hw.memsize'], stdout=subprocessPIPE, close_fds=True).communicate()[0]

        memoire_complet = subprocess.Popen(['vm_stat'], stdout=subprocessPIPE, close_fds=True).communicate()[0]

        # On decoupe notre tableau
        tabmemoire = memoire_complet.splitlines()

        # Puis on va le formater, de la ligne 1 a la ligne 11
        for i in range(1, 12):
            tabmemoire[i] = tabmemoire[i].replace(' ', '')
            tabmemoire[i] = tabmemoire[i].replace('.', '')
            tabmemoire[i] = tabmemoire[i].split(':')

        # Variables specifiques
        mem_free = (int(tabmemoire[1][1]) + int(tabmemoire[4][1])) * float(MacCollector.PAGEBYTES_TO_MBYTES)
        #mem_free = (int(tabmemoire[1][1]) + int(tabmemoire[4][1])) * 0.0039
        mem_active = int(tabmemoire[2][1]) * float(MacCollector.PAGEBYTES_TO_MBYTES)
        mem_inactive = int(tabmemoire[3][1]) * float(MacCollector.PAGEBYTES_TO_MBYTES)
        mem_resident = int(tabmemoire[5][1]) * float(MacCollector.PAGEBYTES_TO_MBYTES)
        mem_swap = int(tabmemoire[11][1]) * float(MacCollector.PAGEBYTES_TO_MBYTES)

        mem_total = (int(tabmemoire[1][1]) + int(tabmemoire[4][1]) + int(tabmemoire[2][1]) + int(tabmemoire[3][1]) + int(tabmemoire[5][1])) * float(MacCollector.PAGEBYTES_TO_MBYTES)

        # Preparing return entity...
        memoryCheck = crEntitiesChecks.Memory()
        memoryCheck.total = mem_total
        memoryCheck.free = mem_free
        memoryCheck.active = mem_active
        memoryCheck.inactive = mem_inactive
        memoryCheck.resident = mem_resident
        memoryCheck.swapTotal = mem_swap

        return memoryCheck

    def get_cpu(self):
        """
            Getting actual CPU utilization.
        """

        # iostat - entrees / sorties
        iostat = subprocess.Popen(['iostat', '-c', '2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

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
            Getting the load average for this computer.
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
            Getting IOStat dictionary.
        """

        # iostat - entrees / sorties
        iostat = subprocess.Popen(['iostat', '-c', '2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers, values))

        return dict_iostat


    def get_uptime(self):
        """
            Gets the number of seconds since the last boot
        """
        uptime_cmd = subprocess.Popen(['sysctl', '-n', 'kern.boottime'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Getting the split dict. The last command return this pattern : { sec = 1353839334, usec = 0 } Sun Nov 25 11:28:54 201)
        # We want to use the first value
        dict_uptime = uptime_cmd.split(' ')

        try:
            timestamp_boot = int(dict_uptime[3].replace(',',''))
        except:
            timestamp_boot = time.time()

        return int(int(time.time()) - int(timestamp_boot))


    def get_disks(self):
        """
            Getting active disks (with disk size for the moment)
        """

        df_dict = subprocess.Popen(['df'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        df_split = df_dict.splitlines()
        header = df_split[0].split()

        # New return entity
        listDisks = crEntitiesHost.Disks()

        for i in range(1, len(df_split)):

            if(df_split[i].startswith('/dev/')):
                line_split = df_split[i].split()
                line_dict = dict(zip(header, line_split))

                # Getting info in MB (Mac OS count with '512 blocks' unit)
                disk_total = int(line_dict['512-blocks']) * MacCollector.BLOCKBYTES_TO_MBYTES
                disk_used = int(line_dict['Used']) * MacCollector.BLOCKBYTES_TO_MBYTES
                disk_free = int(line_dict['Available']) * MacCollector.BLOCKBYTES_TO_MBYTES

                # Getting user friendly name
                # Read http://docs.python.org/2/library/subprocess.html#replacing-shell-pipeline for more informations about shell pipe in Python
                #
                # Full command : diskutil info '+ line_dict['Filesystem'] +' | grep "Media Name" | awk \'BEGIN { FS=":" } END { print $2; }\''
                disk_name_p1 = subprocess.Popen(['diskutil', 'info', line_dict['Filesystem']], stdout = subprocess.PIPE)
                disk_name_p2 = subprocess.Popen(['grep', 'Media Name'], stdin = disk_name_p1.stdout, stdout = subprocess.PIPE)
                disk_name_p1.stdout.close()
                disk_name_p3 = subprocess.Popen(['awk', 'BEGIN { FS=":" } END { print $2; }'], stdin = disk_name_p2.stdout, stdout = subprocess.PIPE).communicate()[0]
                disk_name_p2.stdout.close()

                # Using new check entity
                checkDisk = crEntitiesChecks.Disk()
                checkDisk.date = datetime.datetime.now()
                checkDisk.name = disk_name_p3.lstrip()
                checkDisk.unix_namename = line_dict['Filesystem']
                checkDisk.size = disk_total
                checkDisk.used = disk_used
                checkDisk.free = disk_free

                listDisks.checks.append(checkDisk)

        return listDisks


class DebianCollector(_Collector):

    # Obtenir les infos sur la machine actuelle.
    def get_infos(self):

        # Nom de la machine
        subprocessPIPE = subprocess.PIPE
        hostname = crUtilsText.removeSpecialsCharacters(subprocess.Popen(['hostname', '-s'], stdout=subprocessPIPE, close_fds=True).communicate()[0])

        kernel = crUtilsText.removeSpecialsCharacters(subprocess.Popen(['uname', '-s'], stdout=subprocessPIPE, close_fds=True).communicate()[0])
        kernel_v = crUtilsText.removeSpecialsCharacters(subprocess.Popen(['uname', '-r'], stdout=subprocessPIPE, close_fds=True).communicate()[0])

        hostEntity = crEntitiesHost.Infos()

        hostEntity.uuid = Config.uuid

        hostEntity.os = Config.HOST_CURRENT
        hostEntity.hostname = hostname

        hostEntity.kernelName = kernel
        hostEntity.kernelVersion = kernel_v

        return hostEntity

    # Obtenir les stats CPU.
    # Retourne un dictionnaire de donnees
    def get_cpu(self):
        # vmstat - entrees / sorties
        iostat = subprocess.Popen(['vmstat', '1', '2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

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
            Retourne les stats de la memoire vive de notre host
        """
        memory_result = subprocess.Popen(['cat', '/proc/meminfo'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

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
        memoryCheck = crEntitiesChecks.Memory()
        memoryCheck.total = int(dict_memory['MemTotal']) / 1024
        memoryCheck.free = int(dict_memory['MemFree']) / 1024
        memoryCheck.active = int(dict_memory['Active']) / 1024
        memoryCheck.inactive = int(dict_memory['Inactive']) / 1024
        memoryCheck.resident = 0
        memoryCheck.swapTotal = int(dict_memory['SwapTotal']) / 1024
        memoryCheck.swapFree = int(dict_memory['SwapFree']) / 1024
        memoryCheck.swapUsed = int(float(dict_memory['SwapTotal']) - float(dict_memory['SwapFree'])) / 1024

        return memoryCheck

    # Obtenir les stats LoadAverage
    def get_loadaverage(self):
        """
            Getting load average
        """

        loadavg_result = subprocess.Popen(['cat', '/proc/loadavg'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # On va spliter en fonction des espaces
        dict_loadavg = loadavg_result.split(" ")

        # Prepare return entity
        loadAverageEntity = crEntitiesChecks.LoadAverage()
        loadAverageEntity.last1m = dict_loadavg[0]
        loadAverageEntity.last5m = dict_loadavg[1]
        loadAverageEntity.last15m = dict_loadavg[2]

        loadAverageEntity.uptime = self.get_uptime()

        return loadAverageEntity


    def get_uptime(self):
        """
            Gets the number of seconds since the last boot
        """
        uptime_cmd = subprocess.Popen(['cat', '/proc/uptime'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        uptime_dict = uptime_cmd.split(' ')

        try:
            uptime = int(uptime_dict[0])
        except:
            uptime = int(0)

        return int(uptime)


    def get_disks(self):
        """
            Getting active disks (with disk size for the moment)
        """

        df_dict = subprocess.Popen(['df'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        df_split = df_dict.splitlines()
        header = df_split[0].split()

        # New return entity
        listDisks = crEntitiesHost.Disks()

        for i in range(1, len(df_split)):

            if(df_split[i].startswith('/dev/')):
                line_split = df_split[i].split()

                # Getting info in MB (Linux count with '1K block' unit)
                disk_total = int(line_split[1]) / 1024
                disk_used = int(line_split[2]) / 1024
                disk_free = int(line_split[3]) / 1024

                # Using new check entity
                checkDisk = crEntitiesChecks.Disk()
                checkDisk.date = datetime.datetime.now()
                checkDisk.name = line_split[0]
                checkDisk.size = disk_total
                checkDisk.used = disk_used
                checkDisk.free = disk_free

                listDisks.checks.append(checkDisk)

        return listDisks
