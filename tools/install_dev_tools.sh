#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux dev tools installer
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# This script will install all thirdparties tools (CherryPy, Jinja, etc...) on the current host.
# It's be very helpfull on a dev host.

source ../bash/vars.sh
source ../bash/log.inc.sh
source ../bash/functions.inc.sh

#=============================================================================
# List of libraries to install
# Can be updated as your needs
declare -a LISTE='([0]="CherryPy" [1]="Jinja2" [2]="Routes")'
#=============================================================================
clear

printBox blue "--------------------- CentralReport dev tools installer -----------------------| \
               | \
               Welcome! This script will install development tools on your host.| \
               If you want more details, please visit http://github.com/miniche/CentralReport"

getOS
if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
    printBox red "ERROR!| \
                  The install is only designed for Mac OS, Debian and Ubuntu.| \
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
                          Read the log file in ${ERROR_FILE} for further informations"
            sudo -k
            exit
        fi
    done

    sudo -k

    exit 0

elif [ ${CURRENT_OS} == ${OS_DEBIAN} ]; then
    if [[ $EUID -ne 0 ]]; then
        printBox red "You must be root to install development tools!"
        exit 1
    fi

    printTitle "Installing Setuptools..."

    displayAndExec "Untaring Setuptools..." tar -xzvf ../${SETUPTOOLS_TAR} -C ../thirdparties/
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        printBox red "Woops... Something went wrong untaring Setuptools"
        exit
    fi

    cd ../${SETUPTOOLS_DIR};
    displayAndExec "Installing Setuptools..." python setup.py install
    RETURN_CODE="$?"
    cd ../../;
    if [ ${RETURN_CODE} -ne 0 ]; then
        printBox red "Woops... Something went wrong installing Setuptools"
        exit
    fi

    displayAndExec "Deleting installation files..." rm -Rf ${SETUPTOOLS_DIR}
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        printBox red "Woops... Something went wrong deleting installation files"
        exit
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




