#!/bin/bash

# CentralReport Unix/Linux installer.
# For CentralReport Indev version.
# Be careful! Don't use in production environment!

# Importing some scripts
source bash/vars.sh
source bash/log.inc.sh
source bash/functions.inc.sh
source bash/macos.inc.sh
source bash/debian.inc.sh

# Vars
ACTUAL_MODE=install     # Modes : install, check
unistall_confirm="yes"

# Getting current OS
getOS

# Go!
logFile "-------------- Starting CentralReport uninstaller  --------------"

logConsole "\033[44m\033[1;37m"
logConsole " "
logConsole "-------------- CentralReport uninstaller --------------"
logConsole " "
logConsole "Welcome! This script will uninstall CentralReport on your host."
logConsole "If you want more details, please visit http://github.com/miniche/CentralReport"
logConsole "\033[0m"

getPythonIsInstalled
if [ $? -ne 0 ]; then
    logError "Error, Python must be installed on your host to remove CentralReport."
    exit 1
fi

logConsole " "
read -p "You will uninstall CentralReport. Are you sure to continue (y/n) : " RESP < /dev/tty


# Are you sure to uninstall CR ?
verifyYesNoAnswer ${RESP}
if [ $? -eq 0 ]; then
    logConsole "Processing..."
    logConsole " "

    if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
        logConsole " "
        logError "ERROR"
        logError "The uninstall is only designed for Mac OS and Debian"
        logError "Other Linux distros support coming soon!"

    else
        # 0 = no
        bit_error=0

        if [ ${CURRENT_OS} = ${OS_MAC} ]; then
            # Remove CR from this Mac
            macos_uninstall
            if [ $? -ne 0 ]; then
                bit_error=1
            fi

            # Remove sudo privileges
            sudo -k

        elif [ ${CURRENT_OS} = ${OS_DEBIAN} ]; then

            # Remove CR from this computer
            debian_uninstall
            if [ $? -ne 0 ]; then
                bit_error=1
            fi

        fi

        if [ ${bit_error} -eq 1 ]; then

            logError "Error during CentralReport uninstall..."
            logError "CentralReport may still be installed on this host"

        else
            # Ok, it's done !
            logConsole "\033[1;32m"
            logConsole " "
            logInfo "CentralReport might be deleted on your host."
            logInfo "It's sad, but you're welcome ! :-)"
            logConsole " "
            logInfo "PS : You can write to developers if you found bad things in CentralReport."
            logInfo "You can find them at http://github.com/miniche/CentralReport"
            logInfo "Thanks!"
            logConsole "\033[0m"

        fi
    fi
fi

# End of program
logConsole " "
logInfo " -- End of program -- "
