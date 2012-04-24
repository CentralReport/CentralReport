# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

from collectors.Collector import Collector
from collectors.DebianCollector import DebianCollector
from utils.config import ConfigGetter

#
# Fichier de test - Librement modifiable
#

Collector.getCurrentHost()
configuration = ConfigGetter()

myCollector = DebianCollector()

host_info = DebianCollector.getInfos(myCollector)


print(host_info)
print("--")
print(DebianCollector.getCPU(myCollector))
print("--")
print(DebianCollector.getMemory(myCollector))
print("--")
print(DebianCollector.getLoadAverage(myCollector))