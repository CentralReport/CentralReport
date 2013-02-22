# -*- coding: utf-8 -*-

"""
    CentralReport - Date module
        Contains useful functions to working with dates

    https://github.com/miniche/CentralReport/
"""

import time

import cr.log as crLog


def datetimeToTimestamp(datetime):
    """
        Converts a datetime to Unix timestamp.
    """

    timestamp = 0

    try:
        # Uses the local timestamp
        timestamp = int(time.mktime(datetime.timetuple()))
    except:
        crLog.log_error('Error convert datetime to timestamp')

    return timestamp
