#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# Importing some scripts
source bash/vars.sh
source bash/functions.inc.sh
source bash/uninstall_macos.sh
source bash/uninstall_debian.sh

# Vars
ACTUAL_MODE=install     # Modes : install, check

# Getting current OS
getOS

# Go!

echo -e "\033[44m\033[1;37m"
echo " "
echo "-------------- CentralReport uninstaller --------------"
echo " "
echo "Welcome! This script will uninstall CentralReport on your host."
echo "If you wants more details, please visit http://github.com/miniche/CentralReport"
echo -e "\033[0m"

echo " "
echo "Uninstall"
echo "You will uninstall CentralReport. Are you sure to continue? (Yes/No)"
read

# Are you sure to uninstall CR ?
if [ $REPLY == "yes" ]; then
    echo "OK, continue"
    echo " "

    if [ $CURRENT_OS != "$OS_MAC" ] && [ $CURRENT_OS != $OS_DEBIAN ]; then
        echo " "
        echo -e "\033[1;31mERROR"
        echo -e "\033[0;31mThe uninstall is only design for Mac OS and Debian"
        echo -e "Other Linux distros support coming soon! \033[0m"

    else

        if [ $CURRENT_OS = $OS_MAC ]; then

            # Remove CR from this Mac
            uninstall_from_mac

        elif [ $CURRENT_OS = $OS_DEBIAN ]; then

            # Remove CR from this computer
            uninstall_from_debian

        fi

        # Ok, it's done !
        echo -e "\033[1;32m"
        echo " "
        echo "CentralReport might be deleted on your host."
        echo "It's sad, but you're welcome ! :-)"
        echo " "
        echo "PS : You can write to developers if you found bad things in CentralReport."
        echo "You can find them at http://github.com/miniche/CentralReport"
        echo "Thanks!"
        echo -e "\033[0m"
    fi
fi

# End of program
echo " "
echo " -- End of program -- "