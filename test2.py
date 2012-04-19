import subprocess
import uuid
import urllib
import urllib2
import ConfigParser
import os
import time

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

# Mac OS Wrapper

print('CentralReport - Indev Version - Script test')
print('Mac OS Version')

# Fichier de utils existe ?
config = ConfigParser.ConfigParser()
if os.path.isfile('utils.cfg'):
    print('Fichier de conf : Existant. Lecture.')
else:
    print('Fichier de conf : Inexistant. Creation.')
    
    # On ecrit le fichier de conf
    config.add_section('General')
    config.set('General', 'id', uuid.uuid1())
    config.add_section('Network')
    config.set('Network', 'enable_check_cpu', True)
    config.set('Network', 'enable_check_memory', True)
    config.set('Network', 'enable_check_loadaverage', True)
    config.set("Network", 'server_addr', 'www.charles-emmanuel.me')
    config.write(open('utils.cfg','w'))

# Test fichier de utils
config.read('utils.cfg')
ident = config.get('General', 'id')
config_enable_check_memory = config.getboolean("Network","enable_check_memory")
config_enable_check_cpu = config.getboolean("Network","enable_check_cpu")
config_enable_check_loadaverage = config.getboolean("Network","enable_check_loadaverage")
config_server_addr = config.get("Network",'server_addr')

print('UUID : '+ ident)

while True:
    # Test : optenir des infos sur le systeme

    hostname = subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    #print(cpu)

    uname = subprocess.Popen(['uname','-a'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    #print(cpu)

    kernel = subprocess.Popen(['sysctl','-n','kern.ostype'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    machine = subprocess.Popen(['sysctl','-n','hw.model'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    ncpu = subprocess.Popen(['sysctl','-n','hw.ncpu'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    memsize = subprocess.Popen(['sysctl','-n','hw.memsize'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    architecture = subprocess.Popen(['sysctl','-n','hw.machine'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    # iostat - entrees / sorties
    iostat = subprocess.Popen(['iostat','-c','2'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    # Formatage de iostat
    iostat_split = iostat.splitlines()
    headers = iostat_split[1].split()
    values = iostat_split[3].split()

    # Dictionnaire de valeur
    dict_iostat = dict(zip(headers,values))

    print(str(iostat))
    print(dict_iostat['us'])

    # -- Test memoire
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

    mem_total = (int(tabmemoire[1][1])+int(tabmemoire[2][1])+int(tabmemoire[3][1])+int(tabmemoire[4][1])+int(tabmemoire[5][1]))*4096/1024/1024

    translation = int(tabmemoire[1][1])*4096

    print(translation)
    print("Pages Free : "+ str(int(tabmemoire[1][1])*4096/1024/1024))
    print("Pages Speculative : "+ str(int(tabmemoire[4][1])*4096/1024/1024))
    print("--")
    print("Total : "+ str(mem_total))
    print ("Free : "+ str((int(tabmemoire[1][1]) + int(tabmemoire[4][1]))*4096/1024/1024))
    print("Active : "+ str(int(tabmemoire[2][1])*4096/1024/1024))
    print("Pages Inactive : "+ str(int(tabmemoire[3][1])*4096/1024/1024))
    print("Resident : "+ str(int(tabmemoire[5][1])*4096/1024/1024))


    # -- Fin test memoire


    #cpu = subprocess.Popen(['cat','/proc/version'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    #print(cpu)
    #print(uuid.uuid1())

    error = False

    url = "http://%s/CentralReport/remote.php" % config_server_addr
    values = {'machine' : machine,
              'uuid' : ident,
              'kernel' : kernel,
              'ncpu' : ncpu,
              'architecture' : architecture,
              'language' : 'Python' }

    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()

        print(the_page)

    except Exception as inst:
        error = True
        print("ERREUR : Connexion impossible au serveur : "+ str(inst))



    if error == False and config_enable_check_memory == True:
        # On peut continuer
        url = "http://%s/CentralReport/remote_memory.php" % config_server_addr
        values = {'uuid' : ident,
                  'total' : mem_total,
                  'free' : mem_free,
                  'active' : mem_active,
                  'inactive' : mem_inactive,
                  'resident' : mem_resident }

        try:
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()

            print(the_page)

        except Exception as inst:
            error = True
            print("ERREUR : Connexion impossible au serveur : "+ str(inst))


    if error == False and config_enable_check_cpu == True:
        # On peut continuer

        url = "http://%s/CentralReport/remote_cpu.php" % config_server_addr
        values = {'uuid' : ident,
                  'user' : dict_iostat['us'],
                  'system' : dict_iostat['sy'],
                  'idle' : dict_iostat['id'] }

        try:
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()

            print(the_page)

        except Exception as inst:
            error = True
            print("ERREUR : Connexion impossible au serveur : "+ str(inst))



    if error == False and config_enable_check_loadaverage == True:
        # On peut continuer

        url = "http://%s/CentralReport/remote_ldavg.php" % config_server_addr
        values = {'uuid' : ident,
                  'load1m' : dict_iostat['1m'],
                  'load5m' : dict_iostat['5m'],
                  'load15m' : dict_iostat['15m'] }

        try:
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()

            print(the_page)

        except Exception as inst:
            error = True
            print("ERREUR : Connexion impossible au serveur : "+ str(inst))


    print("Next in 30 seconds")
    # Pause
    time.sleep(30)

# Fin boucle