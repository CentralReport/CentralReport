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

# Online installer script. Will be copied in the "CR_PACKAGES_ROOT" folder
CR_INSTALLER_SCRIPT="utils/online/online_installer.sh"
CR_INSTALLER_SCRIPT_NAME="installer"

# Online uninstaller script. Will be copied in the "CR_PACKAGES_ROOT" folder
CR_UNINSTALLER_SCRIPT="utils/online/online_uninstaller.sh"
CR_UNINSTALLER_SCRIPT_NAME="uninstaller"

if [ ${PWD##*/} != "CentralReport" ]; then
    echo "ERROR - You must be in the project root directory to execute this script."
    exit 1
fi

source tools/packager/functions.inc.sh
source bash/log.inc.sh
source bash/utils.inc.sh

clear
printBox blue "--------------------------- CentralReport packager ----------------------------| \
               | \
               This tool will generate the CentralReport installer/uninstaller package."

if [ $(uname -s) != "Darwin" ]; then
    printBox red "ERROR - One-line packager works only on Mac OS X."
    exit 1
fi

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

# Temporary folders
if [ -d "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}" ]; then
    sudo rm -R "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}"
fi

if [ -d "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}" ]; then
    sudo rm -R "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}"
fi

mkdir "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}"
mkdir "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}"

# Final packages
if [ -f "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_NAME}" ]; then
    sudo rm "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_NAME}"
fi

if [ -f "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_NAME}" ]; then
    sudo rm "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_NAME}"
fi

# Online scripts
if [ -f "${CR_PACKAGES_ROOT}${CR_INSTALLER_SCRIPT_NAME}" ]; then
    sudo rm "${CR_PACKAGES_ROOT}${CR_INSTALLER_SCRIPT_NAME}"
fi

if [ -f "${CR_PACKAGES_ROOT}${CR_INSTALLER_SCRIPT_NAME}" ]; then
    sudo rm "${CR_PACKAGES_ROOT}${CR_INSTALLER_SCRIPT_NAME}"
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
