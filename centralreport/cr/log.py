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

        custom_rotating_fileHandler.setFormatter(_format_logger())

        cr_logger.addHandler(custom_rotating_fileHandler)

        if debug_mode_enabled:
            # In debug mode, we display logs on the standard output too.
            custom_console_handler = logging.StreamHandler(sys.stdout)
            custom_console_handler.setLevel(logging.DEBUG)
            custom_console_handler.setFormatter(_format_logger())

            cr_logger.addHandler(custom_console_handler)

    return cr_logger


def log_debug(text):
    """
        Adds a record at the DEBUG level.
        Useful to write in the config file and on the stdout when debug mode is enabled.
    """
    get_cr_logger().debug(text)


def log_info(text):
    """
        Adds a record at the INFO level.
        Useful at anytime.
    """
    get_cr_logger().info(text)


def log_warning(text):
    """
        Adds a record at the WARNING level.
        Useful when the current process is not breaking the application but requires some attention.
    """
    get_cr_logger().warning(text)


def log_error(text):
    """
        Adds a record at the ERROR level.
        Useful when the current process has to stop but does not require the application to stop too.
    """
    get_cr_logger().error(text)


def log_critical(text):
    """
        Adds a record at the CRITICAL level.
        Useful when the current process forces the application to stop.
    """
    get_cr_logger().critical(text)


def _format_logger():
    """
        Returns the format of the Logger.
    """

    return logging.Formatter(fmt='[%(asctime)s] %(levelname)s: \t %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
