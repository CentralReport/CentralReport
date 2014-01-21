# -*- coding: utf-8 -*-

"""
    CentralReport - Date module
        Contains useful functions to working with dates

    https://github.com/CentralReport
"""

import datetime
import sys


def datetime_to_timestamp(datetime_to_convert):
    """
        Converts a datetime to Unix timestamp.
    """

    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = datetime_to_convert - epoch

    if sys.version_info >= (2, 7):
        return long(delta.total_seconds())
    else:
        return long(delta.days * 86400 + delta.seconds + delta.microseconds / 1e6)
