# -*- coding: utf-8 -*-

# CentralReport - Indev version
# Project by Charles-Emmanuel CAMUS - Avril 2012

#
# Warning: Not used. Only for testing purposes.
#


from sys import path as sysPath
from os import path as osPath

sysPath.insert(0, osPath.abspath(__file__ + '/../../libs/requests-1.1.0.zip'))

import requests

from cr.entities.webservices import WebServiceReturn


class WebServices:
    """
        PS: This class is not used for the moment.
        It has been created for testing purpose only.
    """

    @staticmethod
    def send_json(url, data):
        """
            Sends data to the remote server

            @param url: Destination of the data
            @param data: data to sent

            @return: Response object of the Request library
            @rtype: cr.entities.webservices.WebServiceReturn
        """

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=data, headers=headers)

        ws_return = WebServiceReturn()
        ws_return.code = response.status_code
        ws_return.headers = response.headers
        ws_return.text = response.text

        return ws_return
