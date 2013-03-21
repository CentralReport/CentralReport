# -*- coding: utf-8 -*-

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

#
# Warning: Not used. Only for testing purposes.
#


from sys import path as sysPath
from os import path as osPath
from cr import log

sysPath.insert(0, osPath.abspath(__file__ + '/../../libs/requests-1.1.0.zip'))

import requests


class WebServices:
    """
        PS: This class is not used for the moment.
        It has been created for testing purpose only.
    """

    @staticmethod
    def send_full_check(full):
        url = "http://httpbin.org/post"  # Will be replaced with CentralReport Online IP

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        r = requests.post(url, data=full, headers=headers)
        log.log_debug(r.text)
