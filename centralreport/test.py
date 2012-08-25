# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

import collectors.MacCollector

#
# Fichier de test - Librement modifiable
#

myCollector = collectors.MacCollector.MacCollector()

for disk in myCollector.getDisksInfo():
    print str(disk['filesystem']) +' '+ str(disk['free']) +' MB available on '+ str(disk['total']) +' MB'