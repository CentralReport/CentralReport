#!/bin/bash

### BEGIN INIT INFO
# Provides:          CentralReport
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start CentralReport at boot time
# Description:       Enable service provided by CentralReport Daemon.
### END INIT INFO

# Path to centralreport executable
CENTRALREPORT_BIN=/usr/local/bin/centralreport/centralreport.py

# Carry out specific functions when asked to by the system
case "$1" in
    start)
        echo "Starting CentralReport"
        python ${CENTRALREPORT_BIN} start
        ;;
    stop)
        echo "Stopping CentralReport"
        python ${CENTRALREPORT_BIN} stop
        ;;
    restart)
        echo "Restarting CentralReport"
        python ${CENTRALREPORT_BIN} stop
        sleep 3
        python ${CENTRALREPORT_BIN} start
        echo "CentralReport started"
        ;;
    status)
        python ${CENTRALREPORT_BIN} status
        ;;
    *)
        echo "Usage: /etc/init.d/centralreport.sh {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
