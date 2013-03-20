#!/bin/sh

# ------------------------------------------------------------
# CentralReport Unix/Linux "0.1.0 uninstaller"
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# This script contains functions used to remove CentralReport 0.1.0 from the current host.

#
# Detects if CentralReport 0.1.0 is already installed on this host
#
# PARAMETERS: None
# RETURN:
#     0: CentralReport 0.1.0 is not installed
#     1: CentralReport 0.1.0 is installed
#
function detect_010_version(){

    if [ -f /usr/local/bin/centralreport/centralreport.py ] || [ -f /etc/centralreport.cfg ] || [ -f /etc/init.d/centralreport.sh ]; then
        return 1
    fi

    return 0
}

#
# This function deletes old files from 0.1.0 version
#
# PARAMETERS: None
# RETURN:
#     0: 0.1.0 is successfuly deleted
#     The error code otherwise
#
function delete_010_version(){

    printTitle "Deleting old files from 0.1.0 version..."

    # First, stopping CentralReport daemon
    if [ -f /usr/local/bin/centralreport/centralreport.py ]; then
        displayAndExec "Stopping CentralReport 0.1.0..." execute_privileged_command python /usr/local/bin/centralreport/centralreport.py stop
    fi

    if [ -f /etc/centralreport.cfg ]; then
        displayAndExec "Deleting the old configuration file..." execute_privileged_command rm -f /etc/centralreport.cfg
    else
        logFile "The old configuration file already deleted"
    fi

    # Removing old init.d script
    if [ -f /etc/init.d/centralreport.sh ]; then
        CR_PID=$(cat /var/run/centralreport.pid)
        displayAndExec "Deleting the old init.d script..." execute_privileged_command rm -f /etc/init.d/centralreport.sh

        displayAndExec "Unregistering the init.d service..." execute_privileged_command update-rc.d -f centralreport.sh remove
    fi

    if [ -f /var/run/centralreport.pid ]; then
        # If the PID file has found, we must kill CentralReport daemon before deleting this file!
        CR_PID=$(cat /var/run/centralreport.pid)
        displayAndExec "Killing CentralReport ruthless..." execute_privileged_command kill -9 ${CR_PID}

        displayAndExec "Deleting the old PID file..." execute_privileged_command rm -f /var/run/centralreport.pid
    else
        logFile "The old PID file already deleted"
    fi

    if [ -d /usr/local/bin/centralreport/ ]; then
        displayAndExec "Deleting core scripts and libraries..." execute_privileged_command rm -f -R /usr/local/bin/centralreport/
    else
        logFile "Old core scripts and libraries already deleted..."
    fi

}

