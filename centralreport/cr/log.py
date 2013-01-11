__author__ = 'che'

import logging
import sys


def configLog(enable_debug_mode=False):
    """
        Configures the logging system (executed on time when CentralReport is starting).
    """

    if not enable_debug_mode:
        # Writing only "INFO" or more important messages in a log file (production environement)
        logging.basicConfig(filename='/var/log/centralreport.log',
                            format='%(levelname)s \t %(asctime)s \t %(message)s',
                            level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S')

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
