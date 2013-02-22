# -*- coding: utf-8 -*-

"""
    CentralReport - Date module
        Contains useful functions to working with dates

    https://github.com/miniche/CentralReport/
"""

import time

from cr import log


def datetime_to_timestamp(datetime):
    """
        Converts a datetime to Unix timestamp.
    """

    timestamp = 0

    try:
        # Uses the local timestamp
        timestamp = int(time.mktime(datetime.timetuple()))
    except:
        log.log_error('Error convert datetime to timestamp')

    return timestamp
