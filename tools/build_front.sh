#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux packager
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# This script builds front assets, used with the web server

if [ ${PWD##*/} != "tools" ]; then
    echo "ERROR - You must be in the 'tools' directory to execute this script."
    exit 1
fi

cd ../

npm install
if [ "$?" -ne "0" ]; then
    logError "Error loading npm modules!"
    cd "${CR_PROJECT_ROOT}"

    exit 1
fi

grunt prod
if [ "$?" -ne "0" ]; then
    logError "Error building front assets using grunt!"
    cd "${CR_PROJECT_ROOT}"

    exit 1
fi

cd tools/

exit 0
