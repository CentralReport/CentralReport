# -*- coding: utf-8 -*-

"""
    CentralReport - Web module
        Contains useful functions around the web

    https://github.com/CentralReport
"""

import socket


def check_port(ip, port):
    """
        Checks if the port is open on a specific IP

        @param ip: IP of the remote host
        @param port: The port to check

        @return bool: True if the port is open, False if closed
    """
    socket_port = socket.socket()

    try:
        socket_port.connect((ip, int(port)))
    except socket.error:
        return False
    else:
        socket_port.close()

    return True


