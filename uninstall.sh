#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux uninstaller
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# Importing some scripts
source bash/vars.inc.sh
source bash/log.inc.sh
source bash/utils.inc.sh
source bash/functions.inc.sh

# We are ready to uninstall CentralReport. Log this and print the header.
logFile "-------------- Starting CentralReport uninstaller  --------------"

# Cleaning console and display the header lightbox
clear

printBox blue "------------------------- CentralReport uninstaller ---------------------------| \
               | \
               Welcome! This script will uninstall CentralReport on your host.| \
               If you want more details, please visit http://github.com/miniche/CentralReport"

# Getting current OS to check if uninstall will work for this host
getOS
if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then

    printBox red "ERROR!| \
                  The uninstall is only designed for Mac OS, Debian and Ubuntu.| \
                  Support for other OS will come soon!"

    exit 1
fi

getPythonIsInstalled
if [ $? -ne 0 ]; then
    printBox red "Error! Python must be installed on your host to remove CentralReport."

    exit 1
fi

# On debian, the current user must have administrative privileges.
if [ "${CURRENT_OS}" == "${OS_DEBIAN}" ]; then
    if [[ $EUID -ne 0 ]]; then
        logFile "You must be root to install CentralReport!"
        printBox red "You must be root to install CentralReport!"
        exit 1
    fi
fi

logConsole " "
read -p "You will uninstall CentralReport. Are you sure you want to continue (y/N)? " RESP < /dev/tty

# Are you sure to uninstall CR?
checkYesNoAnswer ${RESP}
if [ $? -eq 0 ]; then
    # 0 = no error during uninstall
    bit_error=0

    if [ ${CURRENT_OS} == ${OS_MAC} ]; then
        logInfo "Processing... CentralReport will be removed from this Mac."

        # On Mac OS, the user must have access to administrative commands.
        # Testing if the "sudo" session still alive...
        sudo -n echo "hey" > /dev/null 2>&1
        if [ "$?" -ne 0 ]; then

            echo -e "\n\nPlease use your administrator password to uninstall CentralReport on this Mac."
            sudo -v
            if [ $? -ne 0 ]; then
                logError "Enable to use root privileges!"
                bit_error=1
            fi
        fi
    elif [ ${CURRENT_OS} == ${OS_DEBIAN} ]; then
        logInfo "Processing... CentralReport will be removed from this Linux."
    fi

    # Process to CentralReport installation...
    if [ ${bit_error} -eq 0 ]; then
        uninstall_cr
        if [ "$?" -ne 0 ]; then
            bit_error=1
        fi
    fi

    if [ ${bit_error} -eq 1 ]; then
        # We display a generic message: previous logs already the specific error message.
        logFile "Error uninstalling CentralReport! CentralReport may still be installed on this host"

        logConsole " "
        printBox red " Error uninstalling CentralReport!| \
                       CentralReport may still be installed on this host| \
                       | \
                       Some logs have been written in ${ERROR_FILE}"

    else
        # Nothing wrong happened while uninstalling. We log this, and then we display the "sad" green lightbox.
        logFile "CentralReport has been deleted from your host."

        # Adding a space before the lightbox to separate previous logs with the success message.
        logConsole " "
        printBox blue "CentralReport has been deleted from your host.| \
                       It's sad, but you're welcome!| \
                       | \
                       PS:| \
                       Thanks for your interest in CentralReport!| \
                       One of the best ways you can help us improve CentralReport is to let us know| \
                       about any problems you could have found.| \
                       You can find CR developers at http://github.com/miniche/CentralReport| \
                       Thanks!"

    fi
else
    logInfo "Uninstall aborted on user demand."
fi

if [ "${CURRENT_OS}" == "${OS_MAC}" ]; then
    # Remove sudo privileges
    sudo -k
fi

logFile " -- End of the uninstall program -- "
exit 0
