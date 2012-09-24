#!/bin/bash

# CentralReport Unix/Linux packager.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# This script package CentralReport in one archive (.tar.gz)

# Works only on Mac OS for now!
if [ $(uname -s) != "Darwin" ]; then
    echo "ERROR - One-line packager works only on Mac OS for now"
    exit 1
fi

cd ../

sudo -v

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
