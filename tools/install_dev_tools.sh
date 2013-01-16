#!/bin/bash

# CentralReport Unix/Linux.
# For CentralReport Indev version.
# By careful! Don't use in production environment!

# This script will install all thirdparties tools (CherryPy, Jinja, etc...) on the current host.
# It's be very helpfull on a dev host.

source ../bash/vars.sh
source ../bash/functions.inc.sh

echo "------------------------------------------"
echo "CentralReport dev tools installer"
echo "------------------------------------------"

# Works only on Mac OS for now!
if [ $(uname -s) != "Darwin" ]; then
    displayError "ERROR - Works only on Mac OS for now"
    exit 1
fi

echo " "
echo "Please use an administrator password to install all tools on this Mac"
sudo -v
if [ $? -ne 0 ]; then
    displayError "ERROR - Incorrect root password. Script aborted."
    exit
fi

cd ../

echo "Installing CherryPy"
echo "Untar CherryPy..."
tar -xzvf ${CHERRYPY_TAR} -C thirdparties/

echo "Installing CherryPy..."
cd ${CHERRYPY_DIR};
sudo python setup.py install
cd ../../;

echo "Deleting install files..."
sudo rm -Rf ${CHERRYPY_DIR}

echo "CherryPy is installed!"
echo " "



# Then, installing Jinja2 Templates...
echo "Installing Jinja2"
echo "Untar Jinja2..."
tar -xzvf ${JINJA_TAR} -C thirdparties/

echo "Installing Jinja2..."
cd ${JINJA_DIR};
sudo python setup.py install
cd ../../;

echo "Deleting install files..."
sudo rm -Rf ${JINJA_DIR}

echo "Jinja2 is installed!"




sudo -k

echo " --- End of the program ---"

exit 0
