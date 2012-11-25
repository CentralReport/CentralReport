#!/bin/bash

### BEGIN INIT INFO
# Provides:          CentralReport
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start CentralReport at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO


# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting CentralReport "
    python /usr/local/bin/centralreport/centralreport.py start
    ;;
  stop)
    echo "Stopping CentralReport"
    python /usr/local/bin/centralreport/centralreport.py stop
    ;;
  restart)
    echo "Restarting CentralReport"
    python /usr/local/bin/centralreport/centralreport.py restart
    ;;
  status)
    python /usr/local/bin/centralreport/centralreport.py status
    ;;
  *)
    echo "Usage: /etc/init.d/centralreport_debian.sh {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0
