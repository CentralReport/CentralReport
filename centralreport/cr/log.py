# -*- coding: utf-8 -*-

"""
    CentralReport - Log module
        Contains log function to work with Python logging modules

    https://github.com/miniche/CentralReport/
"""

import logging
import logging.handlers
import sys


def configLog(enable_debug_mode=False):
    """
        Configures the logging system (executed on time when CentralReport is starting).
    """

    LOG_FILENAME = '/var/log/centralreport.log'

    if not enable_debug_mode:
        # Writing only "INFO" or more important messages in a log file (production environement)
        # TODO: Replace "DEBUG" in production
        logging.basicConfig(filename=LOG_FILENAME,
                            format='%(levelname)s \t %(asctime)s \t %(message)s',
                            level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S')

        # Using python rotating log function
        crLogging = logging.getLogger('centralreport')
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=5, backupCount=5)
        crLogging.addHandler(crLogging)

    else:
        # In debug mode, we only display message on standard output.
        logging.basicConfig(stream=sys.stdout,
                            format='%(levelname)s \t %(asctime)s \t %(message)s',
                            level=logging.DEBUG, datefmt='%m/%d/%Y %H:%M:%S')


def writeDebug(text):
    logging.debug(text)


def writeInfo(text):
    logging.info(text)


def writeError(text):
    logging.error(text)


def writeCritical(text):
    logging.critical(text)


def writeFatal(text):
    logging.fatal(text)
