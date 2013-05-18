#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux online uninstaller
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# This script will download latest CentralReport version and uninstall CR from this host
# It works for Mac OS X, Debian and Ubuntu
# Enjoy!

# Vars
URL_CR="http://files.centralreport.net/cr_uninstaller.tar.gz"
ARCHIVE="cr_uninstaller.tar.gz"
DIR="CentralReportUninstaller"

CURRENT_OS=""
OS_MAC="MacOS"
OS_DEBIAN="Debian"

# TODO: Find a more accurate word than "online"
echo -e "\n\nWelcome to CentralReport online uninstaller!"

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
        exit 2
    fi

else
    echo " "
    echo "Sorry, your OS isn't supported yet..."
    exit 1
fi

echo -e "\nChecking Python availability on your host"
python -V
if [ $? -ne 0 ]; then
    echo -e "\n\nError, Python must be installed on your host to execute CentralReport."
    exit 1
fi

# Downloading the required package...
cd /tmp
if [ ${CURRENT_OS} = ${OS_MAC} ]; then
    curl -O ${URL_CR}
else
    wget -q ${URL_CR}
fi

if [ ! -f ${DIR} ]; then
    echo -e "\n\nError downloading the CentralReport uninstaller!"
    exit 3
fi

# Unpackaging the uninstaller...
tar -xzvf ${ARCHIVE}

cd ${DIR}
chmod +x uninstall.sh

./uninstall.sh

# The uninstallation is now finished, cleaning temporary files...
echo "Removing tmp files"
cd ../
rm -R ${DIR}
rm ${ARCHIVE}

# Done !
exit 0
