# -*- coding: utf-8 -*-

"""
    CentralReport - Web module
        Contains useful functions from around the web

    https://github.com/CentralReport
"""

import socket


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


