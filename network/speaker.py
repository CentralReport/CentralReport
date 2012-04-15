# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

from utils.config import ConfigGetter
import urllib, urllib2

class Speaker:

    @staticmethod
    def sendStats(self,page,stats):

        config_server_addr = ConfigGetter.config.get("Network",'server_addr')

        url = "http://%s/CentralReport/"+ str(page) +".php" % config_server_addr
        values = list(stats)

        try:
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()

            print(the_page)

        except Exception as inst:
            error = True
            print("ERREUR : Connexion impossible au serveur : "+ str(inst))