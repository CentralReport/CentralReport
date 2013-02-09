#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux uninstaller
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# Importing some scripts
source bash/debian.inc.sh
source bash/functions.inc.sh
source bash/log.inc.sh
source bash/macos.inc.sh
source bash/vars.sh

# We are ready to uninstall CentralReport. Log this and print the header.
logFile "-------------- Starting CentralReport uninstaller  --------------"

# Cleaning console and display the header lightbox
clear

printLightBox blue "-------------------------- CentralReport uninstaller ---------------------------"
printLightBox blue " "
printLightBox blue " Welcome! This script will uninstall CentralReport on your host."
printLightBox blue " If you want more details, please visit http://github.com/miniche/CentralReport"
printLightBox blue " "

# Getting current OS to check if uninstall will works for this host
getOS
if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
    printLightBox red " "
    printLightBox red " ERROR!"
    printLightBox red " The install is only designed for Mac OS, Debian and Ubuntu."
    printLightBox red " Support for other OS will come soon!"
    printLightBox red " "

    exit 1
fi

getPythonIsInstalled
if [ $? -ne 0 ]; then
    printLightBox red " "
    printLightBox red " Error! Python must be installed on your host to remove CentralReport."
    printLightBox red " "

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
        # Remove CR from this Mac
        macos_uninstall
        if [ $? -ne 0 ]; then
            bit_error=1
        fi

        # Remove sudo privileges
        sudo -k

    elif [ ${CURRENT_OS} = ${OS_DEBIAN} ]; then
        # Remove CR from this computer
        debian_uninstall
        if [ $? -ne 0 ]; then
            bit_error=1
        fi
    fi

    if [ ${bit_error} -eq 1 ]; then
        logFile "Error uninstalling CentralReport! CentralReport may still be installed on this host"

        printLightBox red " "
        printLightBox red " Error uninstalling CentralReport!"
        printLightBox red " CentralReport may still be installed on this host"
        printLightBox red " "

    else
        # Ok, it's done !
        logFile "CentralReport has been deleted on your host."

        printLightBox green " "
        printLightBox green " CentralReport has been deleted on your host."
        printLightBox green " It's sad, but you're welcome!"
        printLightBox green " "
        printLightBox green " PS: Thanks for your interest in CentralReport!"
        printLightBox green " "
        printLightBox green " One of the best ways you can help us improve CentralReport is to let us know "
        printLightBox green " about any problems you find with it."
        printLightBox green " You can find the developers at http://github.com/miniche/CentralReport"
        printLightBox green " Thanks!"
        printLightBox green " "

    fi
else
    logInfo "Uninstall aborded by user."
fi

# End of program
logConsole " "
logInfo " -- End of the program -- "

exit 0
