# -*- coding: utf-8 -*-

"""
    CentralReport - Log module
        Contains log function to work with Python logging modules

    https://github.com/miniche/CentralReport/
"""

import logging
import logging.handlers
import sys

# Our custom logger object. Initialized on the first use.
crLogger = None
debug_mode_enabled = False


def getCrLogger():
    """
        Gets the Logger object. This function initializes it if it's the first call.
    """

    global crLogger
    global debug_mode_enabled

    if crLogger is None:
        # Using python rotating log function
        crLogger = logging.getLogger()

        logLevel = logging.INFO if debug_mode_enabled is False else logging.DEBUG
        crLogger.setLevel(logLevel)

        # In debug mode, log file must be in "/tmp", due to system permissions.
        logFilename = '/var/log/centralreport.log' if debug_mode_enabled is False else '/tmp/centralreport.log'

        # Max size per log file: 5 MB (1024 * 1024 * 5). Max log files: 2.
        customRotatingFileHandler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=5242880, backupCount=2)
        customRotatingFileHandler.setFormatter(logging.Formatter(fmt='%(levelname)s \t %(asctime)s \t %(message)s',
                                                                 datefmt='%m/%d/%Y %I:%M:%S'))

        crLogger.addHandler(customRotatingFileHandler)

        if debug_mode_enabled:
            # In debug mode, we display logs on the standard output too.
            customConsoleHandler = logging.StreamHandler(stream=sys.stdout)
            customConsoleHandler.setLevel(logging.DEBUG)
            customConsoleHandler.setFormatter(logging.Formatter(fmt='%(levelname)s \t %(asctime)s \t %(message)s',
                                                                datefmt='%m/%d/%Y %I:%M:%S'))

            crLogger.addHandler(customConsoleHandler)

    return crLogger


def writeDebug(text):
    getCrLogger().debug(text)


def writeInfo(text):
    getCrLogger().info(text)


def writeError(text):
    getCrLogger().error(text)


def writeCritical(text):
    getCrLogger().critical(text)


def writeFatal(text):
    getCrLogger().fatal(text)
