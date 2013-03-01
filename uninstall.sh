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
source bash/functions.inc.sh

source bash/debian.inc.sh
source bash/macos.inc.sh

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

logConsole " "
read -p "You will uninstall CentralReport. Are you sure you want to continue (y/N)? " RESP < /dev/tty

# Are you sure to uninstall CR?
checkYesNoAnswer ${RESP}
if [ $? -eq 0 ]; then
    logConsole "Processing..."

    # 0 = no error during uninstall
    bit_error=0

    if [ ${CURRENT_OS} = ${OS_MAC} ]; then
        # Removes CR from this Mac
        macos_uninstall
        if [ $? -ne 0 ]; then
            bit_error=1
        fi

        # Remove sudo privileges
        sudo -k

    elif [ ${CURRENT_OS} = ${OS_DEBIAN} ]; then
        # Removes CR from this Debian/Ubuntu distribution
        debian_uninstall
        if [ $? -ne 0 ]; then
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

# End of program
logConsole " "
logInfo " -- End of the uninstall program -- "

exit 0
