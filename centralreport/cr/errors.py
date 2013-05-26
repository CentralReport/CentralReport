# -*- coding: utf-8 -*-

"""
    CentralReport - Errors module
        Contains all definitions of the CentralReport custom errors

    https://github.com/CentralReport
"""


class CentralReportError(Exception):
    """
        Defines the CentralReport error template.
        Can be inherited by custom subclasses.
    """

    def __init__(self, code, message=''):
        """
            @param code: The error code, must be an integer.
            @param message: Custom message, must be brief and complete the error code.
        """
        self.code = code
        self.message = message


class OnlineError(CentralReportError):
    """
        Defines an error during a communication with CentralReport Online
    """
    pass
