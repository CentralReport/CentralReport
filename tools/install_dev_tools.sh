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

# First, we install CherryPy...
displayAndExec "Installing CherryPy..." sudo easy_install CherryPy
RETURN_CODE="$?"
if [ ${RETURN_CODE} -ne 0 ]; then
    printLightBox red ${RETURN_CODE}
    exit
fi

# Then, installing Jinja2 Templates...
displayAndExec "Installing Jinja 2..." sudo easy_install Jinja2
RETURN_CODE="$?"
if [ ${RETURN_CODE} -ne 0 ]; then
    printLightBox red ${RETURN_CODE}
    exit
fi

# Finally, installing Routes library...
displayAndExec "Installing Routes..." sudo easy_install routes
RETURN_CODE="$?"
if [ ${RETURN_CODE} -ne 0 ]; then
    printLightBox red ${RETURN_CODE}
    exit
fi

sudo -k

echo " --- End of the program ---"

exit 0
