import subprocess, datetime
from utils.config import ConfigGetter
from collectors.Collector import Collector
from utils.TextUtilities import TextUtilities

from entities.CpuCheckEntity import CpuCheckEntity
from entities.MemoryCheckEntity import MemoryCheckEntity
from entities.LoadAverageCheckEntity import LoadAverageCheckEntity
from entities.DiskCheckEntity import DiskCheckEntity
from entities.DisksEntity import DisksEntity
from entities.HostEntity import HostEntity

class MacCollector:
    """
        This collector can execute Mac OS command and get some useful values.
    """

    def getInfos(self):
        """
            Getting some informations on this Mac.
        """

        hostname = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])

        uname = subprocess.Popen(['uname','-a'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        kernel = subprocess.Popen(['sysctl','-n','kern.ostype'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        kernel_v = subprocess.Popen(['uname','-r'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        model = subprocess.Popen(['sysctl','-n','hw.model'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        ncpu = subprocess.Popen(['sysctl','-n','hw.ncpu'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        memsize = subprocess.Popen(['sysctl','-n','hw.memsize'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        architecture = subprocess.Popen(['sysctl','-n','hw.machine'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        cpu_model = subprocess.Popen(['sysctl','-n','machdep.cpu.brand_string'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Using new HostEntity
        hostEntity = HostEntity()

        hostEntity.uuid = ConfigGetter.uuid

        hostEntity.os = Collector.host_current
        hostEntity.hostname = hostname
        hostEntity.architecture = architecture

        hostEntity.model = model

        hostEntity.kernelName = kernel
        hostEntity.kernelVersion = kernel_v

        hostEntity.cpuModel = cpu_model
        hostEntity.cpuCount = ncpu

        return hostEntity



    def getMemory(self):
        """
            Getting memory informations.
        """

        memsize = subprocess.Popen(['sysctl','-n','hw.memsize'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        memoire_complet = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # On decoupe notre tableau
        tabmemoire = memoire_complet.splitlines()

        # Puis on va le formater, de la ligne 1 a la ligne 11
        for i in range(1,12):
            tabmemoire[i] = tabmemoire[i].replace(" ","")
            tabmemoire[i] = tabmemoire[i].replace(".","")
            tabmemoire[i] = tabmemoire[i].split(':')

        # Variables specifiques
        mem_free = (int(tabmemoire[1][1]) + int(tabmemoire[4][1]))*4096/1024/1024
        mem_active = int(tabmemoire[2][1])*4096/1024/1024
        mem_inactive = int(tabmemoire[3][1])*4096/1024/1024
        mem_resident = int(tabmemoire[5][1])*4096/1024/1024
        mem_swap = int(tabmemoire[11][1])*4096/1024/1024

        mem_total = (int(tabmemoire[1][1]) + int(tabmemoire[4][1]) + int(tabmemoire[2][1]) + int(tabmemoire[3][1]) + int(tabmemoire[5][1]))*4096/1024/1024

        # Preparing return entity...
        memoryCheck = MemoryCheckEntity()
        memoryCheck.total = mem_total
        memoryCheck.free = mem_free
        memoryCheck.active = mem_active
        memoryCheck.inactive = mem_inactive
        memoryCheck.resident = mem_resident
        memoryCheck.swapTotal = mem_swap

        return memoryCheck




    def getCPU(self):
        """
        Getting actual CPU utilization.
        """

        # iostat - entrees / sorties
        iostat = subprocess.Popen(['iostat','-c','2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers,values))

        # Use your new CpuCheckEntity!
        cpuCheck = CpuCheckEntity()
        cpuCheck.idle = dict_iostat['id']
        cpuCheck.system = dict_iostat['sy']
        cpuCheck.user = dict_iostat['us']

        return cpuCheck




    def getLoadAverage(self):
        """
            Getting the load average for this computer.
        """

        dict_iostat = self.getIOStat()

        # Prepare return entity
        loadAverageEntity = LoadAverageCheckEntity()
        loadAverageEntity.last1m = dict_iostat['1m']
        loadAverageEntity.last5m = dict_iostat['5m']
        loadAverageEntity.last15m = dict_iostat['15m']

        return loadAverageEntity




    def getIOStat(self):
        """
        Getting IOStat dictionary.
        """

        # iostat - entrees / sorties
        iostat = subprocess.Popen(['iostat','-c','2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers,values))

        return dict_iostat



    def getDisksInfo(self):
        """
        Getting active disks (with disk size for the moment)
        """

        df_dict = subprocess.Popen(['df'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        df_split = df_dict.splitlines()
        header = df_split[0].split()

        # New return entity
        listDisks = DisksEntity()

        for i in range(1,len(df_split)):

            if(df_split[i].startswith("/dev/")):
                line_split = df_split[i].split()
                line_dict = dict(zip(header,line_split))

                # Getting info in MB (Mac OS count with '512 blocks' unit)
                disk_total = int(line_dict['512-blocks'])*512/1024/1024
                disk_used = int(line_dict['Used'])*512/1024/1024
                disk_free = int(line_dict['Available'])*512/1024/1024

                # Using new check entity
                checkDisk = DiskCheckEntity()
                checkDisk.date = datetime.datetime.now()
                checkDisk.name = line_dict['Filesystem']
                checkDisk.size = disk_total
                checkDisk.used = disk_used
                checkDisk.free = disk_free

                listDisks.checks.append(checkDisk)

        return listDisks



