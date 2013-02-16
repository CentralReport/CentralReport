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
enable_debug_mode = False


def getCrLogger():

    global crLogger
    global enable_debug_mode

    if crLogger is None:
        # Using python rotating log function
        crLogger = logging.getLogger()

        # In debug mode, log file must be in "/tmp", due to system permissions.
        logFilename = '/var/log/centralreport.log' if enable_debug_mode is False else '/tmp/centralreport.log'

        crLogger.setLevel(logging.DEBUG)
        customRotatingFileHandler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=6000, backupCount=5)
        customRotatingFileHandler.setFormatter(logging.Formatter(fmt='%(levelname)s \t %(asctime)s \t %(message)s',
                                                                 datefmt='%m/%d/%Y %I:%M:%S'))

        crLogger.addHandler(customRotatingFileHandler)

        if enable_debug_mode:
            customConsoleHandler = logging.StreamHandler(stream=sys.stdout)
            customConsoleHandler.setLevel(logging.DEBUG)
            customConsoleHandler.setFormatter(logging.Formatter(fmt='%(levelname)s \t %(asctime)s \t %(message)s',
                                                                datefmt='%m/%d/%Y %I:%M:%S'))

            crLogger.addHandler(customConsoleHandler)

    return crLogger


def configLog(enable_debug_mode=False):
    """
        Configures the logging system (executed on time when CentralReport is starting).
    """

    LOG_FILENAME = '/var/log/centralreport.log'

    # if not enable_debug_mode:
    #     # Writing only "INFO" or more important messages in a log file (production environement)
    #     # TODO: Replace "DEBUG" in production
    #     # logging.basicConfig(filename=LOG_FILENAME,
    #     #                     format='%(levelname)s \t %(asctime)s \t %(message)s',
    #     #                     level=logging.DEBUG,
    #     #                     datefmt='%m/%d/%Y %I:%M:%S')
    #
    #
    # else:
    #     # In debug mode, we only display message on standard output.
    #     logging.basicConfig(stream=sys.stdout,
    #                         format='%(levelname)s \t %(asctime)s \t %(message)s',
    #                         level=logging.DEBUG,
    #                         datefmt='%m/%d/%Y %H:%M:%S')


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
