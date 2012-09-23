#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# Importing scripts...
source bash/vars.sh
source bash/functions.inc.sh
source bash/macos.inc.sh
source bash/installer_debian.sh

# Vars
ACTUAL_MODE=install                         # Modes : install, check


# Go!

echo -e "\033[44m\033[1;37m"
echo -e "  -------------- CentralReport installer --------------\033[0;44m"
echo " "
echo "  Welcome! This script will install CentralReport on your host."
echo "  If you wants more details, please visit http://github.com/miniche/CentralReport."
echo " "
echo " During installation, we can ask an administrator password. It permit CentralReport "
echo " to write in some directories and remove old CR installations."
echo -e "\033[0m"

# In the future, it will possible to have different modes.
if [ -n "$1" ]; then
    ACTUAL_MODE=$1
fi

# Getting current OS - from common_functions.sh
getOS

# Check the actual mode.
if [ $ACTUAL_MODE = "install" ]; then

    # Right now, it only works on MacOS.
    # Support for Linux distrib coming soon.
    if [ $CURRENT_OS != $OS_MAC ] && [ $CURRENT_OS != $OS_DEBIAN ]; then
        echo " "
        echo -e "\033[1;31mERROR"
        echo -e "\033[0;31mThe install is only design for Mac OS and Debian"
        echo -e "Other Linux distros support coming soon! \033[0m"
    else

        echo " "
        echo "Install mode enabled"
        echo "You will install CentralReport. Are you sure to continue? (Yes/No)"
        read

        # Are you sure to install CR ?
        if [ $REPLY = "yes" ]; then

            # It's an indev version. At each install, we delete everything.

            # O=no error / 1=one or more errors
            bit_error=0

            if [ ${CURRENT_OS} == "$OS_MAC" ]; then
                echo "Ok, I continue. I will install CentralReport on a mac"
                macos_install
                if [ $? -ne 0 ]; then
                    bit_error=1
                fi

            elif [ ${CURRENT_OS} == "$OS_DEBIAN" ]; then
                echo "Ok. I continue. I will install CentralReport on Debian"
                install_on_debian

            fi



            if [ ${bit_error} -eq 1 ]; then

                displayError "Error during CentralReport installation..."
                displayError "CentralReport isn't installed on this host."

            else
                # Done ! We can starting CentralReport!


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
