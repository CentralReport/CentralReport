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

CHERRYPY_TAR=thirdparties/CherryPy.tar.gz
MAKO_TAR=thirdparties/Mako.tar.gz

CHERRYPY_DIR=thirdparties/CherryPy-3.2.2
MAKO_DIR=thirdparties/Mako-0.7.2

# Go!

echo " "
echo "-------------- CentralReport installer --------------"
echo " "
echo "Welcome! This script will install CentralReport on your host."
echo "If you wants more details, please visit http://github.com/miniche/CentralReport"

# In the future, it will possible to have differents modes.
if [ -n "$1" ]; then
    ACTUAL_MODE=$1
fi


# Check the actual mode.
if [ ${ACTUAL_MODE} == "install" ]; then

    echo " "
    echo "Install"
    echo "You will install CentralReport. Are you sure to continue? (Yes/No)"
    read

    # Are you sure to install CR ?
    if [ $REPLY == "yes" ]; then
        echo "OK, continue"
        echo " "

        # It's an indev version. At each install, we delete everything.

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

        echo " "
        echo " ** Starting installation ** "
        echo " "

        echo "Copy CentralReport in the good directory..."
        echo " -- "
        sudo mkdir ${INSTALL_DIR}
        sudo cp -R -f -v centralreport ${PARENT_DIR}
        echo " -- "
        echo "Copy : Done !"


        echo " "
        echo " ** Starting installing thirparties software ** "
        echo " (Please consult http://github.com/miniche/CentralReport for licenses) "
        echo " "


        # First, we install CherryPy
        echo "Installing CherryPy"
        echo "Untar CherryPy..."
        tar -xzvf ${CHERRYPY_TAR} -C thirdparties/

        echo "Installing CherryPy..."
        cd ${CHERRYPY_DIR};
        sudo python setup.py install
        cd ../../;

        echo "Deleting install files..."
        sudo rm -Rf ${CHERRYPY_DIR}

        echo "CherryPy is installed!"
        echo " "



        # Then, installing Mako Templates...
        echo "Installing Mako Templates"
        echo "Untar Mako..."
        tar -xzvf ${MAKO_TAR} -C thirdparties/

        echo "Installing Mako..."
        cd ${MAKO_DIR};
        sudo python setup.py install
        cd ../../;

        echo "Deleting install files..."
        sudo rm -Rf ${MAKO_DIR}

        echo "Mako is installed!"
        echo " "




        # Done ! We can starting CentralReport!


        echo " "
        echo " ** Starting CentralReport... ** "
        sudo python ${INSTALL_DIR}/run.py start
    fi

else
    echo " "
    echo "ERROR!"
    echo "Unknown argument"
    echo "Use : install.sh [install]"
fi


# End of program
echo " "
echo " -- End of program -- "