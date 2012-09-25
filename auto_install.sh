#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# This script will download latest CentralReport version, and begin installation.
# It works for Mac OS X, Debian and Ubuntu
# Enjoy!

# Vars
URL_CR="http://www.charles-emmanuel.me/cr/package.tar.gz"
ARCHIVE="package.tar.gz"
DIR="CentralReportIndev"

CURRENT_OS=""
OS_MAC="MacOS"
OS_DEBIAN="Debian"

echo -e "\n\nWelcome to CentralReport one-line installer!"

# Getting current OS
if [ $(uname -s) == "Darwin" ]; then
    # Mac OS X
    CURRENT_OS=${OS_MAC}
elif [ -f "/etc/debian_version" ] || [ -f "/etc/lsb-release" ]; then
    # Debian or Ubuntu
    CURRENT_OS=${OS_DEBIAN}

    if [[ $EUID -ne 0 ]]; then
        echo " "
        echo "You must be root to run CentralReport installer!"
        exit 1
    fi

else
    echo " "
    echo "Sorry, your distro isn't supported yet..."
    exit 1
fi

# Testing if Python is available on this host
echo -e "\nTesting Python version..."
python -V
if [ $? -eq 0 ]; then
    echo -e "\n\nError, Python must be installed on your host to execute CentralReport."
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
chmod +x install.sh

# Execute installer...
./install.sh

# After install, remove all downloaded files
echo "Removing tmp files"
cd ../
rm -R ${DIR}
rm ${ARCHIVE}

# Done !
exit 0
