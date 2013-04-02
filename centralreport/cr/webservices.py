# -*- coding: utf-8 -*-

"""
    CentralReport - Webservices module
        Contains functions used to manage webservices

    https://github.com/miniche/CentralReport/
"""

from sys import path as sysPath
from os import path as osPath

sysPath.insert(0, osPath.abspath(__file__ + '/../../libs/requests-1.1.0.zip'))
import requests

from cr.entities.webservices import Answer


METHOD_GET = "GET"
METHOD_POST = "POST"
METHOD_PUT = "PUT"
METHOD_PATCH = "PATCH"
METHOD_DELETE = "DELETE"


def send_data(method, url, data='', headers=''):
    """
        Sends data to the remote server

        @param method: The HTTP method to use. Please see "WebServices.METHOD_xxxx" constants.
        @param url: Destination of the data
        @param data: data to sent
        @param headers: Custom header to use

        @return: Response object of the Request library
        @rtype: cr.entities.webservices.Answer
    """

    if method == METHOD_GET:
        response = requests.get(url, data=data, headers=headers)
    elif method == METHOD_POST:
        response = requests.post(url, data=data, headers=headers)
    elif method == METHOD_PUT:
        response = requests.put(url, data=data, headers=headers)
    elif method == METHOD_PATCH:
        response = requests.patch(url, data=data, headers=headers)
    elif method == METHOD_DELETE:
        response = requests.delete(url, data=data, headers=headers)
    else:
        raise ValueError('Unknown verb')

    ws_return = Answer()
    ws_return.code = response.status_code
    ws_return.headers = response.headers
    ws_return.text = response.text

    return ws_return


def send_json(method, url, data):
    """
        Sends JSON to the remote server

        @param method: The HTTP method to use. Please see "WebServices.METHOD_xxxx" constants.
        @param url: Destination of the data
        @param data: data to sent

        @return: Response object of the Request library
        @rtype: cr.entities.webservices.Answer
    """

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return send_data(method, url, data, headers)

