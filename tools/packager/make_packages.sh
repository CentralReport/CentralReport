#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux packager
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# This script generate the installer and the uninstaller packages.
# They will be used for the online tools. Please see "online_installer.sh" and "online_uninstaller.sh" scripts.

CR_PACKAGES_ROOT=/tmp/cr-package/

CR_PACKAGE_INSTALLER_FOLDER=CentralReportInstaller/
CR_PACKAGE_INSTALLER_NAME=cr_installer.tar.gz

CR_PACKAGE_UNINSTALLER_FOLDER=CentralReportUninstaller/
CR_PACKAGE_UNINSTALLER_NAME=cr_uninstaller.tar.gz

if [ ${PWD##*/} != "packager" ]; then
    echo "ERROR - You must be in the 'packager' directory to execute this script."
    exit 1
fi

source functions.inc.sh
source ../../bash/log.inc.sh
source ../../bash/utils.inc.sh

clear
printBox blue "--------------------------- CentralReport packager ----------------------------| \
               | \
               This tool will generate the CentralReport installer/uninstaller package."

if [ $(uname -s) != "Darwin" ]; then
    printBox red "ERROR - One-line packager works only on Mac OS X."
    exit 1
fi

cd ../../
CR_PROJECT_ROOT=$(pwd)

logConsole "Please use your administrator password to generate the package"
sudo -v
if [ $? -ne 0 ]; then
    printBox red "ERROR - Incorrect root password. Script aborted."
    exit 1
fi

clear
printBox blue "Generating CentralReport packages..."

logConsole "Preparing directories and cleaning old packages..."

if [ ! -d ${CR_PACKAGES_ROOT} ]; then
    logConsole "Creating the generation folder..."
    mkdir ${CR_PACKAGES_ROOT}
fi

if [ -d "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}" ]; then
    sudo rm -R "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}"
fi

if [ -d "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}" ]; then
    sudo rm -R "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}"
fi

mkdir "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}"
mkdir "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}"

if [ -f "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_NAME}" ]; then
    sudo rm "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_NAME}"
fi

if [ -f "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_NAME}" ]; then
    sudo rm "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_NAME}"
fi

# We must update the IFS variable. The default separator in bash is the space.
# In the whitelist and the blacklist, the separator is the carriage return.
IFS_SAVED=$IFS
IFS=$'\n'

ERROR_CREATING_PACKAGE=false
create_packages
if [ "$?" -ne 0 ]; then
    ERROR_CREATING_PACKAGE=true
fi

IFS=${IFS_SAVED}

logConsole "Removing the temporary folders..."

sudo rm -R "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}"
sudo rm -R "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}"

logConsole "Killing the sudo session..."
sudo -k

open ${CR_PACKAGES_ROOT}

if [ ${ERROR_CREATING_PACKAGE} == true ]; then
    printBox red "An error has occured. Please consult the previous logs for more details."
    exit 1
fi

printBox blue "Packages created successfully!"

exit 0
