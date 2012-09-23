#!/bin/bash

# ONLY FOR MAC OS X YET!!!

# CentralReport Unix/Linux uninstaller.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# This script will download latest CentralReport version, and begin uninstall on current host.
# Enjoy!

# Vars
URL_CR="http://www.charles-emmanuel.me/cr/package.tar.gz"
ARCHIVE="package.tar.gz"
DIR="CentralReportIndev"

# Download full package...
curl -O ${URL_CR}

# Unpackage...
tar -xzvf ${ARCHIVE}

# Go to new dir...
cd ${DIR}
chmod +x uninstall.sh

# Execute installer...
./uninstall.sh

# After install, remove all downloaded files
echo "Removing tmp files"
cd ../
rm -R ${DIR}
rm ${ARCHIVE}

# Done !
