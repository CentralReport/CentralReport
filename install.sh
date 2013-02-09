#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash installer
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# Importing scripts...
source bash/vars.sh
source bash/log.inc.sh
source bash/functions.inc.sh
source bash/macos.inc.sh
source bash/debian.inc.sh

# Modes: only "install" yet ("check" mode will be added soon)
ACTUAL_MODE=install

# We are ready to uninstall CentralReport. Log this and print the header.
logFile "-------------- Starting CentralReport installer  --------------"

# Cleaning console and display the lightbox
clear

printLightBox blue  "--------------------------- CentralReport installer ----------------------------"
printLightBox blue  " "
printLightBox blue  " Welcome! This script will install CentralReport on your host."
printLightBox blue  " If you want more details, please visit http://github.com/miniche/CentralReport"
printLightBox blue  " "
printLightBox blue  " When installing CentralReport, we may ask for your password."
printLightBox blue  " It will allow CentralReport to write files and directories such as"
printLightBox blue  " the project binaries, logs, etc."
printLightBox blue  " "

# In the future, it will be possible to have different modes.
if [ -n "$1" ]; then
    ACTUAL_MODE=$1
fi

# Right now, CentralReport is only available on Mac OS X, Debian and Ubuntu.
# Others Linux distributions coming soon.
getOS
if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
    printLightBox red " "
    printLightBox red " ERROR!"
    printLightBox red " The install is only designed for Mac OS, Debian and Ubuntu."
    printLightBox red " Support for other OS will come soon!"
    printLightBox red " "

    exit 1
fi

# Python is mandatory for CentralReport
getPythonIsInstalled
if [ $? -ne 0 ]; then
    printLightBox red " "
    printLightBox red " Error! Python must be installed on your host to execute CentralReport."
    printLightBox red " "

    exit 1
fi

# Check the actual mode.
if [ "install" == ${ACTUAL_MODE} ]; then
    logConsole " "
    read -p "You will install CentralReport. Are you sure you want to continue (y/N): " RESP < /dev/tty

    # Are you sure to install CR ?
    checkYesNoAnswer ${RESP}
    if [ $? -eq 0 ]; then
        # O=no error / 1=one or more errors
        bit_error=0

        if [ ${CURRENT_OS} == ${OS_MAC} ]; then
            logInfo "Processing... CentralReport will be installed on this Mac."
            macos_install
            if [ $? -ne 0 ]; then
                bit_error=1
            fi

        elif [ ${CURRENT_OS} == ${OS_DEBIAN} ]; then
            logInfo "Processing... CentralReport will be installed on this Linux."
            debian_install
            if [ $? -ne 0 ]; then
                bit_error=1
            fi

        fi

        if [ ${bit_error} -eq 1 ]; then
            printLightBox red " "
            printLightBox red  " Something went wrong when installing CentralReport!"
            printLightBox red  " CentralReport isn't installed on this host."
            printLightBox red " "

            logFile "Something went wrong when installing CentralReport, consult previous log."

        else
            # Displays the success text!
            logFile "CentralReport is now installed! For more options, you can edit the config file at /etc/centralreport.cfg"
            logFile "More help at http://github.com/miniche/CentralReport. Have fun!"

            printLightBox green " "
            printLightBox green " CentralReport is now installed!"
            printLightBox green " For more options, you can edit the config file at /etc/centralreport.cfg"
            printLightBox green " "
            printLightBox green " You can find more help at http://github.com/miniche/CentralReport."
            printLightBox green " Have fun!"
            printLightBox green " "

        fi
     else
        logInfo "Installation aborded by user demand."
    fi
else
    printLightBox red  " "
    printLightBox red  " ERROR!"
    printLightBox red  " Unknown argument"
    printLightBox red  " Use: install.sh [install]"
    printLightBox red  " "
fi

# End of program
logConsole " "
logInfo " -- End of the program -- "

exit 0
