#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux dev tools installer
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# This script will install all thirdparties tools (CherryPy, Jinja, etc...) on the current host.
# It's be very helpfull on a dev host.

source ../bash/vars.inc.sh
source ../bash/log.inc.sh
source ../bash/utils.inc.sh
source ../bash/functions.inc.sh

#=============================================================================
# List of libraries to install
# Can be updated based on your needs
declare -a LISTE='([0]="flask")'
#=============================================================================
clear

printBox blue "--------------------- CentralReport dev tools installer -----------------------| \
               | \
               Welcome! This script will install development tools on your host.| \
               If you want more details, | \
               please visit http://github.com/CentralReport/CentralReport"

getOS
if [ ${CURRENT_OS} == "${OS_OTHER}" ]; then
    printBox red "ERROR!| \
                  Installation is only designed for Mac OS, Debian and Ubuntu.| \
                  Support for other OS will come soon!"
    exit 1
fi

if [ ${CURRENT_OS} == ${OS_MAC} ]; then
    echo " "
    echo " Please use an administrator password to install all tools on this Mac"
    sudo -v

    if [ $? -ne 0 ]; then
        printBox red "ERROR - Incorrect root password. Script aborted."
        exit
    fi

    printTitle "Installing Libraries..."

    for i in ${!LISTE[*]}
    do
        displayAndExec "Installing ${LISTE[${i}]}..." sudo easy_install ${LISTE[${i}]}
        RETURN_CODE="$?"
        if [ ${RETURN_CODE} -ne 0 ]; then
            printBox red "Woops... Something went wrong installing ${LISTE[${i}]}| \
                          Read the log file in ${ERROR_FILE} for further information"
            sudo -k
            exit
        fi
    done

    sudo -k
    exit 0

elif [ ${CURRENT_OS} == ${OS_DEBIAN} ] && [ ${CURRENT_OS} == ${OS_CENTOS} ]; then
    if [[ $EUID -ne 0 ]]; then
        printBox red "You must be root to install development tools!"
        exit 1
    fi

    printTitle "Installing Libraries..."

    for i in ${!LISTE[*]}
    do
        displayAndExec "Installing ${LISTE[${i}]}..." easy_install ${LISTE[${i}]}
        RETURN_CODE="$?"
        if [ ${RETURN_CODE} -ne 0 ]; then
            printBox red "Woops... Something went wrong installing ${LISTE[${i}]}| \
                          Read the log file in ${ERROR_FILE} for further informations"
            exit
        fi
    done
fi




