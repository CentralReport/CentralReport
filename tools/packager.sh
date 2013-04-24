#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux packager
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# This script package CentralReport in one archive (.tar.gz)
# This archive is to be placed on the CR website and working with "online_installer" and "online_uninstaller"


# Works only on Mac OS for now!
if [ $(uname -s) != "Darwin" ]; then
    echo "ERROR - One-line packager works only on Mac OS for now"
    exit 1
fi

# You must be in "CentralReport directory to execute this script
if [ ${PWD##*/} != "tools" ]; then
    echo "ERROR - You must be in the CentralReport directory to execute this script."
    exit 1
fi

cd ../../

sudo -v
if [ $? -ne 0 ]; then
    echo "ERROR - Incorrect root password. Script aborted."
    exit
fi

echo "Generating CentralReport full package..."

if [ -d "CentralReportIndev" ]; then
    sudo rm -R CentralReportIndev
fi

if [ -f "package.tar.gz" ]; then
    sudo rm package.tar.gz
fi

sudo cp -R CentralReport CentralReportIndev

# Remove all .pyc files
cd CentralReportIndev
find . -name "*.pyc" -exec sudo rm -rf {} \;
cd ../

sudo rm -R CentralReportIndev/.git
sudo rm -R CentralReportIndev/.idea
sudo rm -R CentralReportIndev/.DS_Store

sudo tar -czvf package.tar.gz CentralReportIndev/

sudo rm -R CentralReportIndev

sudo -k

echo "Package created successfully!"

exit 0
