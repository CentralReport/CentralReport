#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# Importing some scripts
source bash/common_functions.sh
source bash/uninstall_macos.sh

# Vars
ACTUAL_MODE=install     # Modes : install, check
PARENT_DIR=/usr/local/bin/
INSTALL_DIR=/usr/local/bin/centralreport
CONFIG_FILE=/etc/cr/centralreport.cfg
PID_FILE=/tmp/daemon-centralreport.pid
STARTUP_PLIST=/Library/LaunchDaemons/com.centralreport.plist

# Getting current OS
getOS

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

    if [ "$CURRENT_OS" != "$OS_MAC" ]; then
        echo " "
        echo -e "\033[1;31mERROR"
        echo -e "\033[0;31mThe install is only design for Mac OS"
        echo -e "Linux support coming soon! \033[0m"

     else
        # Remove CR from this Mac

        uninstall_from_mac
    fi

    # Ok, it's done !
    echo " "
    echo "CentralReport might be deleted on your host."
    echo "It's sad, but you're welcome ! :-)"
    echo " "
    echo "PS : You can write to developers if you found bad things in CentralReport."
    echo "You can find them at http://github.com/miniche/CentralReport"
    echo "Thanks!"

fi

# End of program
echo " "
echo " -- End of program -- "