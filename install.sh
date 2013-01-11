#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# Be careful! Don't use in production environment!

# Importing scripts...
source bash/vars.sh
source bash/log.inc.sh
source bash/functions.inc.sh
source bash/macos.inc.sh
source bash/debian.inc.sh

# Vars
ACTUAL_MODE=install                         # Modes : install, check
install_confirm="yes"

# Go!
writeLog "-------------- Starting CentralReport installer  --------------"

writeConsole "\033[44m\033[1;37m"
writeConsole "  -------------- CentralReport installer --------------"
writeConsole "\033[0;44m"
writeConsole "  Welcome! This script will install CentralReport on your host."
writeConsole "  If you want more details, please visit http://github.com/miniche/CentralReport."
writeConsole " "
writeConsole " When installing CentralReport, we may ask for your password. It will allow CentralReport to write files
            and directories such as the project binaries, logs, etc."
writeConsole "\033[0m"

# In the future, it will be possible to have different modes.
if [ -n "$1" ]; then
    ACTUAL_MODE=$1
fi

# Python is mandatory for CentralReport
getPythonIsInstalled
if [ $? -ne 0 ]; then
    writeError "Error, Python must be installed on your host to execute CentralReport."
    exit 1
fi

# Getting current OS - from common_functions.sh
getOS

# Check the actual mode.
if [ "install" == ${ACTUAL_MODE} ]; then

    # Right now, it only works on MacOS.
    # Support for Linux distrib coming soon.
    if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
        writeError " "
        writeError "ERROR"
        writeError "The install is only designed for Mac OS, Debian and Ubuntu."
        writeError "Other Linux distros support coming soon!"
    else

        writeConsole " "
        writeConsole "Install mode enabled"
        read -p "You will install CentralReport. Are you sure to continue (y/n) : " RESP < /dev/tty

        # Are you sure to install CR ?
        verifyYesNoAnswer ${RESP}
        if [ $? -eq 0 ]; then

            # It's an indev version. At each install, we delete everything.

            # O=no error / 1=one or more errors
            bit_error=0

            if [ ${CURRENT_OS} == ${OS_MAC} ]; then
                writeInfo "Processing... CentralReport will be installed on this Mac."
                macos_install
                if [ $? -ne 0 ]; then
                    bit_error=1
                fi

            elif [ ${CURRENT_OS} == ${OS_DEBIAN} ]; then
                writeInfo "Processing... CentralReport will be installed on this Linux."
                debian_install
                if [ $? -ne 0 ]; then
                    bit_error=1
                fi

            fi


            if [ ${bit_error} -eq 1 ]; then

                writeError "Something went wrong when installing CentralReport!"
                writeError "CentralReport isn't installed on this host."

            else

                # Displays the success text!
                writeConsole "\033[1;32m"
                writeConsole " "
                writeInfo "CentralReport is now installed!"
                writeInfo "For more options, you can edit the config file at /etc/centralreport.cfg"
                writeConsole " "
                writeInfo "More help at http://github.com/miniche/CentralReport"
                writeInfo "Have fun!"
                writeConsole " "
                writeConsole "\033[0m"

            fi

        fi

    fi

else
    writeError " "
    writeError "ERROR!"
    writeError "Unknown argument"
    writeError "Use : install.sh [install]"
fi


# End of program
writeConsole " "
writeInfo " -- End of program -- "
