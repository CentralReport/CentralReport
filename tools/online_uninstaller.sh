#!/bin/bash

# CentralReport Unix/Linux uninstaller.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# This script will download latest CentralReport version, and begin uninstall on current host.
# It works for Mac OS X, Debian and Ubuntu
# Enjoy!

# Vars
URL_CR="http://www.charles-emmanuel.me/cr/package.tar.gz"
ARCHIVE="package.tar.gz"
DIR="CentralReportIndev"

CURRENT_OS=""
OS_MAC="MacOS"
OS_DEBIAN="Debian"

# Getting current OS
if [ "Darwin" == $(uname -s) ]; then
    # Mac OS X
    CURRENT_OS=${OS_MAC}
elif [ -f "/etc/debian_version" ] || [ -f "/etc/lsb-release" ]; then
    # Debian or Ubuntu
    CURRENT_OS=${OS_DEBIAN}

    if [[ $EUID -ne 0 ]]; then
        echo " "
        echo "You must be root to run CentralReport uninstaller!"
        exit 1
    fi

else
    echo " "
    echo "Sorry, your OS isn't supported yet..."
    exit 1
fi

# Download full package...
if [ ${CURRENT_OS} = ${OS_MAC} ]; then
    curl -O ${URL_CR}
else
    wget -q ${URL_CR}
fi

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
exit 0
