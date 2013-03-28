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

    VERB_GET = "GET"
    VERB_POST = "POST"
    VERB_PUT = "PUT"
    VERB_PATCH = "PATCH"
    VERB_DELETE = "DELETE"

    @staticmethod
    def send_data(verb, url, data, headers):
        """
            Sends data to the remote server

            @param verb: The HTTP verb to use. Please see "WebServices.VERB_xxxx" constants.
            @param url: Destination of the data
            @param data: data to sent
            @param headers: Custom header to use

            @return: Response object of the Request library
            @rtype: cr.entities.webservices.WebServiceReturn
        """

        if verb == WebServices.VERB_GET:
            response = requests.get(url, data=data, headers=headers)
        elif verb == WebServices.VERB_POST:
            response = requests.post(url, data=data, headers=headers)
        elif verb == WebServices.VERB_PUT:
            response = requests.put(url, data=data, headers=headers)
        elif verb == WebServices.VERB_PATCH:
            response = requests.patch(url, data=data, headers=headers)
        elif verb == WebServices.VERB_DELETE:
            response = requests.delete(url, data=data, headers=headers)
        else:
            raise ValueError('Unknown verb')

        ws_return = WebServiceReturn() 
        ws_return.code = response.status_code
        ws_return.headers = response.headers
        ws_return.text = response.text

        return ws_return

    @staticmethod
    def send_json(verb, url, data):
        """
            Send JSON to the remote server

            @param verb: The HTTP verb to use. Please see "WebServices.VERB_xxxx" constants.
            @param url: Destination of the data
            @param data: data to sent

            @return: Response object of the Request library
            @rtype: cr.entities.webservices.WebServiceReturn
        """

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return WebServices.send_data(verb, url, data, headers)

