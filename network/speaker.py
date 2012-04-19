# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

from utils.config import ConfigGetter
import urllib, urllib2

class Speaker:

    page_INFOS = "remote.php"
    page_CPU = "remote_cpu.php"
    page_MEMORY = "remote__memory.php"
    page_LOADAVERAGE = "remote_ldavg.php"

    @staticmethod
    def sendStats(page,datas):

        config_server_addr = ConfigGetter.config_server_addr

        url = "http://%s/CentralReport/%s" % (str(config_server_addr), str(page))

        #DEBUG
        print("URL : "+ url)
        #values = list(stats)

        try:
            data = urllib.urlencode(datas)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()

            print(the_page)
            return the_page

        except Exception as inst:
            error = True
            print("ERREUR : Connexion impossible au serveur : "+ str(inst))