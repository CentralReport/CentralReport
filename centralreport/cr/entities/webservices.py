# -*- coding: utf-8 -*-

"""
    CentralReport - Webservices module
        Contains all entities used with webservices.

    https://github.com/CentralReport/
"""


class Answer:
    """
        This entity contains the result of a webservice
    """

    def __init__(self):
        self.code = 0
        self.headers = []
        self.text = ""

