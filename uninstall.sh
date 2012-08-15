#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# By careful! Don't use in production environment!


# Vars
ACTUAL_MODE=install     # Modes : install, check
PARENT_DIR=/usr/local/bin/
INSTALL_DIR=/usr/local/bin/centralreport
CONFIG_FILE=/etc/cr/centralreport.cfg
PID_FILE=/tmp/daemon-centralreport.pid
STARTUP_PLIST=/Library/LaunchDaemons/com.centralreport.plist

# Go!

echo " "
echo "-------------- CentralReport uninstaller --------------"
echo " "
echo "Welcome! This script will uninstall CentralReport on your host."
echo "If you wants more details, please visit http://github.com/miniche/CentralReport"

echo " "
echo "Uninstall"
echo "You will uninstall CentralReport. Are you sure to continue? (Yes/No)"
read

# Are you sure to uninstall CR ?
if [ $REPLY == "yes" ]; then
    echo "OK, continue"
    echo " "

    # Check if CentralReport is already running!
    echo "Checking if CentralReport is already running"
    if [ -f ${PID_FILE} ]; then
        echo "CentralReport is already running! Trying to stop it..."
        sudo python ${INSTALL_DIR}/run.py stop
        echo "Done!"
    fi

    # We check if we found datas about CentralReport
    echo "Checking if install directory already exist"
    if [ -d ${INSTALL_DIR} ]; then
        echo "Remove existing install directory"
        sudo rm -rfv $INSTALL_DIR
        echo "Done!"
    fi

    echo "Checking if a config file already exist"
    if [ -f ${CONFIG_FILE} ]; then
        echo "Remove existing config file"
        sudo rm -fv $CONFIG_FILE
        echo "Done!"
    fi

    echo "Checking if the startup plist already exist"
    if [ -f ${STARTUP_PLIST} ]; then
        echo "Remove existing startup plist"
        sudo rm -rfv $STARTUP_PLIST
        echo "Done!"
    fi

    # Ok, it's done !
    echo " "
    echo "CentralReport might be deleted on your host."
    echo "It's sad, but you're welcome ! :-)"
    echo " "
    echo "PS : You can write to developer if you found bad things in CentralReport."
    echo "You can find them at http://github.com/miniche/CentralReport"
    echo "Thanks!"

fi

# End of program
echo " "
echo " -- End of program -- "