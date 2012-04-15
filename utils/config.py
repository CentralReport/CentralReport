# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

__author__ = 'che'

import collectors.Collector
import ConfigParser

def configGetter():

    config = ConfigParser.ConfigParser()
    chemin = ""

    if collectors.Collector.isMac():
        chemin = ""
    else:
        # On est sur un systeme unix
        chemin = "/etc/cr/"


    # Fichier de utils existe ?
    config = ConfigParser.ConfigParser()
    if os.path.isfile(chemin +'utils.cfg'):
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
        config.write(open(chemin +'utils.cfg','w'))

    # Lecture du fichier de utils
    config.read('utils.cfg')
