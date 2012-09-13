#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

function uninstall_from_debian(){

    # Use root account
    if [ $(whoami) != 'root' ]; then
        su root
    fi

    # Check if CentralReport is already running!
    echo "Checking if CentralReport is already running"
    if [ -f ${PID_FILE} ]; then
        echo "CentralReport is already running! Trying to stop it..."
        python ${INSTALL_DIR}/run.py stop
        echo "Done!"

        # Wait before CR is really stopped
        echo "Waiting few seconds until CentralReport daemon is really stopped..."
        sleep 3;
    fi

    # We check if we found datas about CentralReport
    echo "Checking if install directory already exist"
    if [ -d ${INSTALL_DIR} ]; then
        echo "Remove existing install directory"
        rm -rfv $INSTALL_DIR
        echo "Done!"
    fi

    echo "Checking if a config file already exist"
    if [ -f ${CONFIG_FILE} ]; then
        echo "Remove existing config file"
        rm -fv $CONFIG_FILE
        echo "Done!"
    fi

    echo "Checking if the startup script already exist"
    if [ -f ${STARTUP_DEBIAN} ]; then
        echo "Unregister startup script form update-rc.d"
        update-rc.d -f ${STARTUP_DEBIAN} remove
        echo "Remove existing startup script"
        rm -rfv $STARTUP_DEBIAN
        echo "Done!"
    fi

}
