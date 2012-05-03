import subprocess
from utils.config import ConfigGetter
from collectors.Collector import Collector
from utils.TextUtilities import TextUtilities

__author__ = 'che'

class DebianCollector:

    # Obtenir les infos sur la machine actuelle.
    def getInfos(self):

        # Nom de la machine
        hostname = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])

        kernel = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['uname','-s'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])
        kernel_v = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['uname','-r'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])


        return {'os' : Collector.host_current, 'hostname' : hostname, 'uuid' : ConfigGetter.uuid, 'kernel' : kernel, 'kernel_v' : kernel_v, 'language' : 'Python' }


    # Obtenir les stats CPU.
    # Retourne un dictionnaire de donnees
    def getCPU(self):
        # vmstat - entrees / sorties
        iostat = subprocess.Popen(['vmstat','1','2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Formatage de vmstat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers,values))

        return { 'user' : dict_iostat['us'], 'system' : dict_iostat['sy'], 'idle' : dict_iostat['id']}


    def getMemory(self):
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

        return { 'mem_size' : dict_memory['MemTotal'], 'mem_free' : dict_memory['MemFree'], 'mem_active' : dict_memory['Active'], 'mem_inactive' : dict_memory['Inactive'], 'swap_total' : dict_memory['SwapTotal'], 'swap_free' : dict_memory['SwapFree']  }




    # Obtenir les stats LoadAverage
    def getLoadAverage(self):

        loadavg_result = subprocess.Popen(['cat','/proc/loadavg'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # On va spliter en fonction des espaces
        dict_loadavg = loadavg_result.split(" ")


        return {'load1m' : dict_loadavg[0], 'load5m' : dict_loadavg[1], 'load15m' : dict_loadavg[2] }