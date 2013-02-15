# -*- coding: utf-8 -*-

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

#
# Warning: Not used. Only for testing purposes.
#

import urllib
import urllib2
from cr.tools import Config


class Speaker:

    """
        PS: This class is not used for the moment.
        It has been created for testing purpose only.
    """

    PAGE_INFOS = 'remote.php'
    PAGE_CPU = 'remote_cpu.php'
    PAGE_MEMORY = 'remote__memory.php'
    PAGE_LOADAVERAGE = 'remote_ldavg.php'

    @staticmethod
    def sendStats(page, datas):
        config_server_addr = Config.config_server_addr
        url = 'http://%s/CentralReport/%s' % (str(config_server_addr), str(page))
        error = False

        # DEBUG

        print 'URL: %s' % url

        # values = list(stats)

        try:
            data = urllib.urlencode(datas)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()
            print the_page

            return the_page
        except Exception as inst:
            error = True
            print('ERREUR: Connexion impossible au serveur: %s' % inst)
