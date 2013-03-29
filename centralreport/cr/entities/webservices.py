# -*- coding: utf-8 -*-

"""
    CentralReport - Webservices module
        Contains all entities used with webservices.

    https://github.com/miniche/CentralReport/
"""


class Full:
    """
        This entity contains every host information
    """

    def __init__(self):
        self.checks = list()
        self.host = None


class Registration:
    """
        Entity used to get the host status on the remote server
    """

    def __init__(self):
        self.uuid = ""
        self.key = ""
        self.hostname = ""
        self.os = ""
        self.os_version = ""


class Answer:
    """
        This entity contains the result of a webservice
    """

    def __init__(self):
        self.code = 0
        self.headers = []
        self.text = ""

