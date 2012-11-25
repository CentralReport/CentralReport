#
# CentralReport - Indev version
#

import calendar
import cr.log as crLog


def datetimeToTimestamp(datetime):
    """
        Convert a datetime to Unix timestamp (simple, but this function may be very useful)
    """

    # return value
    timestamp = 0

    try:
        timestamp = int(calendar.timegm(datetime.utctimetuple()))
    except:
        crLog.writeError('Error convert datetime to timestamp')

    return timestamp
