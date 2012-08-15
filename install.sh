#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# Vars
ACTUAL_MODE=install                         # Modes : install, check
PARENT_DIR=/usr/local/bin/
INSTALL_DIR=/usr/local/bin/centralreport
CONFIG_FILE=/etc/cr/centralreport.cfg
PID_FILE=/tmp/daemon-centralreport.pid

# Temp install directories.
CHERRYPY_TAR=thirdparties/CherryPy.tar.gz
MAKO_TAR=thirdparties/Mako.tar.gz

CHERRYPY_DIR=thirdparties/CherryPy-3.2.2
MAKO_DIR=thirdparties/Mako-0.7.2

# OS
CURRENT_OS=
OS_MAC="MacOS"
OS_DEBIAN="Debian"


# Go!

echo -e "\033[44m\033[1;37m"
echo -e "  -------------- CentralReport installer --------------\033[0;44m"
echo " "
echo "  Welcome! This script will install CentralReport on your host."
echo "  If you wants more details, please visit http://github.com/miniche/CentralReport"
echo -e "\033[0m"

# In the future, it will possible to have different modes.
if [ -n "$1" ]; then
    ACTUAL_MODE=$1
fi

# Getting actual OS (Linux distrib or Unix OS)
if [ $(uname -s) == "Darwin" ]; then
    CURRENT_OS=${OS_MAC}
fi

# Check the actual mode.
if [ ${ACTUAL_MODE} == "install" ]; then

    # Right now, it only works on MacOS.
    # Support for Linux distrib coming soon.
    if [ "$CURRENT_OS" != "$OS_MAC" ]; then
        echo " "
        echo -e "\033[1;31mERROR"
        echo -e "\033[0;31mThe install is only design for Mac OS"
        echo -e "Linux support coming soon! \033[0m"
    else

        echo " "
        echo "Install mode enabled"
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

            echo " "
            echo "Please wait before the first check..."

            sleep 3;

            echo -e "\033[1;32m"
            echo " "
            echo "CentralReport might be installed!"
            echo "You can go to http://127.0.0.1:8080 to display the web view"
            echo "or you can edit the config file at /etc/cr/centralreport.cfg"
            echo " "
            echo "More help at http://github.com/miniche/CentralReport"
            echo "Have fun!"
            echo " "
            echo -e "\033[0m"

        fi

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