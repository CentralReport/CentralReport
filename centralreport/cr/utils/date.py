#
# CentralReport - Indev version
#

import cr.log as crLog
import time


def datetimeToTimestamp(datetime):
    """
        Converts a datetime to Unix timestamp.
    """

    timestamp = 0

    try:
        # First solution : timestamp UTC
        #timestamp = int(calendar.timegm(datetime.timetuple()))

        # Second solution : local timestamp
        timestamp = int(time.mktime(datetime.timetuple()))
    except:
        crLog.writeError('Error convert datetime to timestamp')

    return timestamp
