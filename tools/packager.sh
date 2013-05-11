#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux packager
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# This script package CentralReport in one archive (.tar.gz)
# This archive is to be placed on the CR website and working with "online_installer" and "online_uninstaller"

if [ ${PWD##*/} != "tools" ]; then
    echo "ERROR - You must be in the 'tools' directory to execute this script."
    exit 1
fi

source ../bash/vars.inc.sh
source ../bash/log.inc.sh
source ../bash/utils.inc.sh
source ../bash/functions.inc.sh

CR_PACKAGES_ROOT=/tmp/cr-package/

CR_PACKAGE_INSTALLER_FOLDER=CentralReportInstaller/
CR_PACKAGE_INSTALLER_NAME=cr_installer.tar.gz

CR_PACKAGE_UNINSTALLER_FOLDER=CentralReportUninstaller/
CR_PACKAGE_UNINSTALLER_NAME=cr_uninstaller.tar.gz

clear
printBox blue "--------------------------- CentralReport packager ----------------------------| \
               | \
               This tool will generate the CentralReport installer/uninstaller package."

if [ $(uname -s) != "Darwin" ]; then
    printBox red "ERROR - One-line packager works only on Mac OS X."
    exit 1
fi

cd ../

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

logConsole "Preparing the installer package..."

# The whitelist contains all files or directory needed for the installer package
for line in $(cat ./tools/packager/installer_whitelist.txt);
do
    if [[ ${line} != "#"* ]] && [[ ${line} != ";"* ]] ; then
        if [ -d ${line} ]; then
            sudo cp -R ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}${line}"
        elif [ -f ${line} ]; then
            sudo cp ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}${line}"
        else
            logError "Missing file or directory: ${line}"
        fi
    fi
done

# The blacklist contains all files or directory unneeded for the installer package
for line in $(cat ./tools/packager/installer_blacklist.txt);
do
    if [[ ${line} == "*"* ]] ; then
        find "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}" -name "${line}" -exec sudo rm -rf {} \;
    elif [[ ${line} != "#"* ]] && [[ ${line} != ";"* ]] ; then
        if [ -d ${line} ]; then
            sudo rm -R ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}${line}"
        elif [ -f ${line} ]; then
            sudo rm ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_INSTALLER_FOLDER}${line}"
        else
            logError "Missing file or directory: ${line}"
        fi
    fi
done

logConsole "Preparing the uninstaller package..."

# The whitelist contains all files or directory needed for the uninstaller package
for line in $(cat ./tools/packager/uninstaller_whitelist.txt);
do
    if [[ ${line} != "#"* ]] && [[ ${line} != ";"* ]] ; then
        if [ -d ${line} ]; then
            sudo cp -R ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}${line}"
        elif [ -f ${line} ]; then
            sudo cp ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}${line}"
        else
            logError "Missing file or directory: ${line}"
        fi
    fi
done

# The blacklist contains all files or directory unneeded for the uninstaller package
for line in $(cat ./tools/packager/uninstaller_blacklist.txt);
do
    if [[ ${line} == "*"* ]] ; then
        find "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}" -name "${line}" -exec sudo rm -rf {} \;
    elif [[ ${line} != "#"* ]] && [[ ${line} != ";"* ]] ; then
        if [ -d ${line} ]; then
            sudo rm -R ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}${line}"
        elif [ -f ${line} ]; then
            sudo rm ${line} "${CR_PACKAGES_ROOT}${CR_PACKAGE_UNINSTALLER_FOLDER}${line}"
        else
            logError "Missing file or directory: ${line}"
        fi
    fi
done

IFS=${IFS_SAVED}

cd ${CR_PACKAGES_ROOT}

logConsole "Creating the installer package..."
sudo tar -czf ${CR_PACKAGE_INSTALLER_NAME} ${CR_PACKAGE_INSTALLER_FOLDER}

logConsole "Creating the uninstaller package..."
sudo tar -czf ${CR_PACKAGE_UNINSTALLER_NAME} ${CR_PACKAGE_UNINSTALLER_FOLDER}

logConsole "Removing the temporary folders..."
sudo rm -R ${CR_PACKAGE_INSTALLER_FOLDER}
sudo rm -R ${CR_PACKAGE_UNINSTALLER_FOLDER}

logConsole "Killing the sudo session..."
#sudo -k

open ${CR_PACKAGES_ROOT}

printBox blue "Package created successfully!"

exit 0
