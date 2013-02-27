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
# List of library to install
# Can be updated as your needs
declare -a LISTE='([0]="CherryPy" [1]="Jinja2" [2]="Routes")'
#=============================================================================

printLightBox blue "------------------------------------------"
printLightBox blue "CentralReport dev tools installer"
printLightBox blue "------------------------------------------"

# Works only on Mac OS for now!
if [ $(uname -s) != "Darwin" ]; then
    printLightBox red "ERROR - Works only on Mac OS for now"
    exit 1
fi

echo " "
echo "Please use an administrator password to install all tools on this Mac"
sudo -v

if [ $? -ne 0 ]; then
    printLightBox red "ERROR - Incorrect root password. Script aborted."
    exit
fi

for i in ${!LISTE[*]}
do
    displayAndExec "Installing ${LISTE[${i}]}..." sudo easy_install ${LISTE[${i}]}
    RETURN_CODE="$?"
    if [ ${RETURN_CODE} -ne 0 ]; then
        printLightBox red "Woops... Something went wrong with the installation of ${LISTE[${i}]}"
        printLightBox red "Read the log file in ${ERROR_FILE} for further informations"
        sudo -k
        exit
    fi
done

sudo -k

exit 0
