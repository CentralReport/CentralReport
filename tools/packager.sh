#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux packager
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# This script package CentralReport in one archive (.tar.gz)
# This archive is to be placed on the CR website and working with "online_installer" and "online_uninstaller"

source ../bash/vars.inc.sh
source ../bash/log.inc.sh
source ../bash/utils.inc.sh
source ../bash/functions.inc.sh

clear
printBox blue "--------------------------- CentralReport packager ----------------------------| \
               | \
               This tool will generate the CentralReport installer/uninstaller package."

# Works only on Mac OS for now!
if [ $(uname -s) != "Darwin" ]; then
    printBox red "ERROR - One-line packager works only on Mac OS X."
    exit 1
fi

# You must be in "CentralReport directory to execute this script
if [ ${PWD##*/} != "tools" ]; then
    printBox red "ERROR - You must be in the 'tools' directory to execute this script."
    exit 1
fi

cd ../../

logConsole "Please use your administrator password to generate the package"
sudo -v
if [ $? -ne 0 ]; then
    printBox red "ERROR - Incorrect root password. Script aborted."
    exit 1
fi

clear
printBox blue "Generating CentralReport full package..."

if [ -d "CentralReportPackage" ]; then
    sudo rm -R CentralReportPackage
fi

if [ -f "package.tar.gz" ]; then
    sudo rm package.tar.gz
fi

logConsole "Copying CentralReport in a temporary folder..."
sudo cp -R CentralReport CentralReportPackage

logConsole "Removing all .pyc files..."
cd CentralReportPackage
find . -name "*.pyc" -exec sudo rm -rf {} \;
cd ../

logConsole "Removing useless dot files..."
sudo rm -R CentralReportPackage/.git 2>/dev/null
sudo rm -R CentralReportPackage/.idea 2>/dev/null
sudo rm -R CentralReportPackage/.DS_Store 2>/dev/null

logConsole "Creating the final package..."
sudo tar -czf package.tar.gz CentralReportPackage/

logConsole "Removing the temporary folder..."
sudo rm -R CentralReportPackage

logConsole "Kill the sudo session..."
sudo -k

printBox blue "Package created successfully!"

exit 0
