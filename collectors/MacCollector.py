import subprocess, datetime
from utils.config import ConfigGetter
from collectors.Collector import Collector
from utils.TextUtilities import TextUtilities

class MacCollector:


    # Obtenir les infos sur la machine actuelle.
    def getInfos(self):
        hostname = TextUtilities.removeSpecialsCharacters(subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE, close_fds=True).communicate()[0])

        #print(cpu)

        uname = subprocess.Popen(['uname','-a'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        #print(cpu)

        kernel = subprocess.Popen(['sysctl','-n','kern.ostype'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        kernel_v = subprocess.Popen(['uname','-r'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        model = subprocess.Popen(['sysctl','-n','hw.model'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        ncpu = subprocess.Popen(['sysctl','-n','hw.ncpu'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        memsize = subprocess.Popen(['sysctl','-n','hw.memsize'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
        architecture = subprocess.Popen(['sysctl','-n','hw.machine'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        cpu_model = subprocess.Popen(['sysctl','-n','machdep.cpu.brand_string'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        return {'os' : Collector.host_current, 'hostname' : hostname, 'model' : model, 'uuid' : ConfigGetter.uuid, 'kernel' : kernel, 'kernel_v' : kernel_v, 'ncpu' : ncpu, 'architecture' : architecture, 'modelcpu' : cpu_model, 'language' : 'Python' }


    # Obtenir les stats memoires
    # Retourne un dictionnaire de donnees.
    def getMemory(self):
        memsize = subprocess.Popen(['sysctl','-n','hw.memsize'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        memoire_complet = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # On decoupe notre tableau
        tabmemoire = memoire_complet.splitlines()
        # Puis on va le formater, de la ligne 1 a la ligne 5
        for i in range(1,6):
            tabmemoire[i] = tabmemoire[i].replace(" ","")
            tabmemoire[i] = tabmemoire[i].replace(".","")
            tabmemoire[i] = tabmemoire[i].split(':')

        # Variables specifiques
        mem_free = (int(tabmemoire[1][1]) + int(tabmemoire[4][1]))*4096/1024/1024
        mem_active = int(tabmemoire[2][1])*4096/1024/1024
        mem_inactive = int(tabmemoire[3][1])*4096/1024/1024
        mem_resident = int(tabmemoire[5][1])*4096/1024/1024

        mem_total = mem_free + mem_active + mem_inactive + mem_resident

        # On retourne un dictionnaire
        return {'date': datetime.datetime.now(), 'mem_size' : float(memsize), 'mem_total' : mem_total ,'mem_free' : mem_free, 'mem_active' : mem_active, 'mem_inactive' : mem_inactive, 'mem_resident' : mem_resident }


    # Obtenir les stats CPU.
    # Retourne un dictionnaire de donnees
    def getCPU(self):
        # iostat - entrees / sorties
        iostat = subprocess.Popen(['iostat','-c','2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers,values))

        return {'date': datetime.datetime.now() ,'user' : dict_iostat['us'], 'system' : dict_iostat['sy'], 'idle' : dict_iostat['id']}


    # Obtenir les stats LoadAverage
    def getLoadAverage(self):

        dict_iostat = self.getIOStat()

        return {'date' : datetime.datetime.now() ,'load1m' : dict_iostat['1m'], 'load5m' : dict_iostat['5m'], 'load15m' : dict_iostat['15m'] }


    # Obtenir le dictionnaire IOStat
    def getIOStat(self):

        # iostat - entrees / sorties
        iostat = subprocess.Popen(['iostat','-c','2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

        # Formatage de iostat
        iostat_split = iostat.splitlines()
        headers = iostat_split[1].split()
        values = iostat_split[3].split()

        # Dictionnaire de valeur
        dict_iostat = dict(zip(headers,values))

        return dict_iostat