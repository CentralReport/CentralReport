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

printLightBox blue "---------------------- CentralReport dev tools installer -----------------------"
printLightBox blue  " "
printLightBox blue  " Welcome! This script will install development tools on your host."
printLightBox blue  " If you want more details, please visit http://github.com/miniche/CentralReport"
printLightBox blue  " "

getOS
if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
    printLightBox red " "
    printLightBox red " ERROR!"
    printLightBox red " The install is only designed for Mac OS, Debian and Ubuntu."
    printLightBox red " Support for other OS will come soon!"
    printLightBox red " "

    exit 1
fi

if [ ${CURRENT_OS} == ${OS_MAC} ]; then
    echo " "
    echo " Please use an administrator password to install all tools on this Mac"
    sudo -v

    if [ $? -ne 0 ]; then
        printLightBox red " "
        printLightBox red " ERROR - Incorrect root password. Script aborted."
        printLightBox red " "
        exit
    fi

    printTitle "Installing Libraries..."

    for i in ${!LISTE[*]}
    do
        displayAndExec "Installing ${LISTE[${i}]}..." sudo easy_install ${LISTE[${i}]}
        RETURN_CODE="$?"
        if [ ${RETURN_CODE} -ne 0 ]; then
            printLightBox red " "
            printLightBox red " Woops... Something went wrong installing ${LISTE[${i}]}"
            printLightBox red " Read the log file in ${ERROR_FILE} for further informations"
            printLightBox red " "
            sudo -k
            exit
        fi
    done

    sudo -k

    exit 0

elif [ ${CURRENT_OS} == ${OS_DEBIAN} ]; then
    if [[ $EUID -ne 0 ]]; then
        printLightBox red " "
        printLightBox red " You must be root to install development tools!"
        printLightBox red " "
        exit 1
    fi

    printTitle "Installing Setuptools..."

    displayAndExec "Untaring Setuptools..." tar -xzvf ../${SETUPTOOLS_TAR} -C ../thirdparties/
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        printLightBox red " "
        printLightBox red " Woops... Something went wrong untaring Setuptools"
        printLightBox red " "
        exit
    fi

    cd ../${SETUPTOOLS_DIR};
    displayAndExec "Installing Setuptools..." python setup.py install
    RETURN_CODE="$?"
    cd ../../;
    if [ ${RETURN_CODE} -ne 0 ]; then
        printLightBox red " "
        printLightBox red " Woops... Something went wrong installing Setuptools"
        printLightBox red " "
        exit
    fi

    displayAndExec "Deleting installation files..." rm -Rf ${SETUPTOOLS_DIR}
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        printLightBox red " "
        printLightBox red " Woops... Something went wrong deleting installation files"
        printLightBox red " "
        exit
    fi

    printTitle "Installing Libraries..."

    for i in ${!LISTE[*]}
    do
        displayAndExec "Installing ${LISTE[${i}]}..." easy_install ${LISTE[${i}]}
        RETURN_CODE="$?"
        if [ ${RETURN_CODE} -ne 0 ]; then
            printLightBox red " "
            printLightBox red " Woops... Something went wrong installing ${LISTE[${i}]}"
            printLightBox red " Read the log file in ${ERROR_FILE} for further informations"
            printLightBox red " "
            exit
        fi
    done
fi




