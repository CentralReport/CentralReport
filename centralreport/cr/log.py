# -*- coding: utf-8 -*-

"""
    CentralReport - Log module
        Contains log functions to work with native Python logging modules

    https://github.com/miniche/CentralReport/
"""

import logging
import logging.handlers
import sys

# Our custom logger object. Initialized on the first use.
cr_logger = None
debug_mode_enabled = False


def get_cr_logger():
    """
        Gets the Logger object. This function initializes it if it's the first call.
    """

    global cr_logger
    global debug_mode_enabled

    if cr_logger is None:
        # Using native python functions to manage logs
        cr_logger = logging.getLogger()

        log_level = logging.INFO if debug_mode_enabled is False else logging.DEBUG
        cr_logger.setLevel(log_level)

        # In debug mode, log file must be in "/tmp", due to system permissions.
        log_filename = '/var/log/centralreport.log' if debug_mode_enabled is False else '/tmp/centralreport.log'

        # Max size per log file: 5 MB (1024 * 1024 * 5). 2 files will be kept as archive.
        custom_rotating_fileHandler = logging.handlers.RotatingFileHandler(log_filename,
                                                                           maxBytes=5242880,
                                                                           backupCount=2)

        custom_rotating_fileHandler.setFormatter(logging.Formatter(fmt='%(levelname)s \t %(asctime)s \t %(message)s',
                                                                   datefmt='%m/%d/%Y %I:%M:%S'))

        cr_logger.addHandler(custom_rotating_fileHandler)

        if debug_mode_enabled:
            # In debug mode, we display logs on the standard output too.
            custom_console_handler = logging.StreamHandler(stream=sys.stdout)
            custom_console_handler.setLevel(logging.DEBUG)
            custom_console_handler.setFormatter(logging.Formatter(fmt='%(levelname)s \t %(asctime)s \t %(message)s',
                                                                  datefmt='%m/%d/%Y %I:%M:%S'))

            cr_logger.addHandler(custom_console_handler)

    return cr_logger


def writeDebug(text):
    """
        Writes a debug message. Only useful for testing and debugging purposes.
        Only written in config file and stdout when debug mode is enabled.
    """
    get_cr_logger().debug(text)


def writeInfo(text):
    """
        Writes a standard message. Will be written in the current log file.
    """
    get_cr_logger().info(text)


def writeError(text):
    """
        Writes an error message: an abnormal situation, but non-critical.
        Will be written in the current log file.
    """
    get_cr_logger().error(text)


def writeCritical(text):
    """
        Writes a critical error. This error requires to stop the current action.
        Will be written in the current log file.
    """
    get_cr_logger().critical(text)


def writeFatal(text):
    """
        Writes a fatal error. This error requires to stop current application.
        Will be written in the current log file.
    """
    get_cr_logger().fatal(text)
