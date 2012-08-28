#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

function uninstall_from_debian(){

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

    echo "Checking if the startup script already exist"
    if [ -f ${STARTUP_DEBIAN} ]; then
        echo "Unregister startup script form update-rc.d"
        sudo update-rc.d -f ${STARTUP_DEBIAN} remove
        echo "Remove existing startup script"
        sudo rm -rfv $STARTUP_DEBIAN
        echo "Done!"
    fi

}
