import subprocess
from utils.config import ConfigGetter
from collectors.Collector import Collector

__author__ = 'che'

class DebianCollector:

    # Obtenir les infos sur la machine actuelle.
    def getInfos(self):
        return {}

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
