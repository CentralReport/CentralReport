#
# CentralReport - Indev version
#

import time
import calendar
import cr.log as crLog


def datetimeToTimestamp(datetime):
    """
        Convert a datetime to Unix timestamp (simple, but this function may be very useful)
    """

    # return value
    timestamp = 0

    try:
        # First solution : timestamp UTC
        #timestamp = int(calendar.timegm(datetime.timetuple()))

        # Second solution : local timestamp
        timestamp = int(time.mktime(datetime.timetuple()))
    except:
        crLog.writeError('Error convert datetime to timestamp')

    return timestamp
