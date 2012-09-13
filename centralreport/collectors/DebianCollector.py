import subprocess
from utils.CRConfig import CRConfig
from collectors.Collector import Collector
from utils.TextUtilities import TextUtilities
from entities.HostEntity import HostEntity
from entities.CpuCheckEntity import CpuCheckEntity
from entities.MemoryCheckEntity import MemoryCheckEntity
from entities.LoadAverageCheckEntity import LoadAverageCheckEntity
from entities.DisksEntity import DisksEntity

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

        # Return entity
        diskEntity = DisksEntity()

        return diskEntity