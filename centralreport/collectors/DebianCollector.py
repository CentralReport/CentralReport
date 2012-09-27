import subprocess,datetime
from utils.CRConfig import CRConfig
from collectors.Collector import Collector
from utils.TextUtilities import TextUtilities
from entities.HostEntity import HostEntity
from entities.CpuCheckEntity import CpuCheckEntity
from entities.MemoryCheckEntity import MemoryCheckEntity
from entities.LoadAverageCheckEntity import LoadAverageCheckEntity
from entities.DisksEntity import DisksEntity
from entities.DiskCheckEntity import DiskCheckEntity

__author__ = 'che'

class DebianCollector(Collector):

    # Obtenir les infos sur la machine actuelle.
    def get_infos(self):

        # Nom de la machine
        hostname = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])

        kernel = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['uname','-s'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])
        kernel_v = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['uname','-r'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])


        # Using new HostEntity
        hostEntity = HostEntity()

        hostEntity.uuid = CRConfig.uuid

        hostEntity.os = CRConfig.HOST_CURRENT
        hostEntity.hostname = hostname
        #hostEntity.architecture = architecture

        #hostEntity.model = model

        hostEntity.kernelName = kernel
        hostEntity.kernelVersion = kernel_v

        #hostEntity.cpuModel = cpu_model
        #hostEntity.cpuCount = ncpu

        return hostEntity



    # Obtenir les stats CPU.
    # Retourne un dictionnaire de donnees
    def get_cpu(self):
        # vmstat - entrees / sorties
        iostat = subprocess.Popen(['vmstat','1','2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Formatage de vmstat
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



    def get_memory(self):
        """
        Retourne les stats de la memoire vive de notre host
        """
        memory_result = subprocess.Popen(['cat','/proc/meminfo'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # On decoupe toutes les lignes
        memory_result_split = memory_result.splitlines()

        # On prepare nos deux listes qui vont servir de modele "cle-valeur"
        list_headers = []
        list_values = []

        # On va parcourir toutes les lignes afin d'obtenir le detail
        for current_line in memory_result_split:
            current_line = current_line.split(":")

            # Suppression des caracteres indesirables
            current_line_values = current_line[1].replace(" ","")
            current_line_values = current_line_values.replace("kB","")

            # Ajout dans nos listes
            list_headers.append(current_line[0])
            list_values.append(current_line_values)

        # Creation de notre dictionnaire
        dict_memory = dict(zip(list_headers,list_values))

        # Preparing return entity...
        memoryCheck = MemoryCheckEntity()
        memoryCheck.total = int(dict_memory['MemTotal'])/1024
        memoryCheck.free = int(dict_memory['MemFree'])/1024
        memoryCheck.active = int(dict_memory['Active'])/1024
        memoryCheck.inactive = int(dict_memory['Inactive'])/1024
        memoryCheck.resident = 0
        memoryCheck.swapTotal = int(dict_memory['SwapTotal'])/1024
        memoryCheck.swapFree = int(dict_memory['SwapFree'])/1024
        memoryCheck.swapUsed = int(float(dict_memory['SwapTotal']) - float(dict_memory['SwapFree']))/1024

        return memoryCheck




    # Obtenir les stats LoadAverage
    def get_loadaverage(self):

        loadavg_result = subprocess.Popen(['cat','/proc/loadavg'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # On va spliter en fonction des espaces
        dict_loadavg = loadavg_result.split(" ")


        # Prepare return entity
        loadAverageEntity = LoadAverageCheckEntity()
        loadAverageEntity.last1m = dict_loadavg[0]
        loadAverageEntity.last5m = dict_loadavg[1]
        loadAverageEntity.last15m = dict_loadavg[2]

        return loadAverageEntity


    def get_disks(self):
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

                # Getting info in MB (Linux count with '1K block' unit)
                disk_total = int(line_split[1])/1024
                disk_used = int(line_split[2])/1024
                disk_free = int(line_split[3])/1024

                # Using new check entity
                checkDisk = DiskCheckEntity()
                checkDisk.date = datetime.datetime.now()
                checkDisk.name = line_split[0]
                checkDisk.size = disk_total
                checkDisk.used = disk_used
                checkDisk.free = disk_free

                listDisks.checks.append(checkDisk)

        return listDisks