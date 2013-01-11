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
writeLog "-------------- Starting CentralReport uninstaller  --------------"

writeConsole "\033[44m\033[1;37m"
writeConsole " "
writeConsole "-------------- CentralReport uninstaller --------------"
writeConsole " "
writeConsole "Welcome! This script will uninstall CentralReport on your host."
writeConsole "If you want more details, please visit http://github.com/miniche/CentralReport"
writeConsole "\033[0m"

getPythonIsInstalled
if [ $? -ne 0 ]; then
    writeError "Error, Python must be installed on your host to remove CentralReport."
    exit 1
fi

writeConsole " "
read -p "You will uninstall CentralReport. Are you sure to continue (y/n) : " RESP < /dev/tty


# Are you sure to uninstall CR ?
verifyYesNoAnswer ${RESP}
if [ $? -eq 0 ]; then
    writeConsole "Processing..."
    writeConsole " "

    if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
        writeConsole " "
        writeError "ERROR"
        writeError "The uninstall is only designed for Mac OS and Debian"
        writeError "Other Linux distros support coming soon!"

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

            writeError "Error during CentralReport uninstall..."
            writeError "CentralReport may still be installed on this host"

        else
            # Ok, it's done !
            writeConsole "\033[1;32m"
            writeConsole " "
            writeInfo "CentralReport might be deleted on your host."
            writeInfo "It's sad, but you're welcome ! :-)"
            writeConsole " "
            writeInfo "PS : You can write to developers if you found bad things in CentralReport."
            writeInfo "You can find them at http://github.com/miniche/CentralReport"
            writeInfo "Thanks!"
            writeConsole "\033[0m"

        fi
    fi
fi

# End of program
writeConsole " "
writeInfo " -- End of program -- "
