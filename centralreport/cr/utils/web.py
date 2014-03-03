# -*- coding: utf-8 -*-

"""
    CentralReport - Web module
        Contains useful functions from around the web

    https://github.com/CentralReport
"""

import socket

import requests

from cr.entities.webservices import Answer

METHOD_GET = "GET"
METHOD_POST = "POST"
METHOD_PUT = "PUT"
METHOD_PATCH = "PATCH"
METHOD_DELETE = "DELETE"


def check_port(ip, port, timeout=None):
    """
        Checks if the port is open on a specific IP

        @param ip: IP of the remote host
        @param port: The port to check
        @param timeout: Timeout, in seconds

        @return bool: True if the port is open, False if closed
    """
    socket_port = socket.socket()

    if timeout is not None:
        socket_port.settimeout(timeout)

    try:
        socket_port.connect((ip, int(port)))
    except socket.error:
        return False
    else:
        socket_port.close()

    return True


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
