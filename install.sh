#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash installer
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

# Importing scripts...
source bash/vars.inc.sh
source bash/log.inc.sh
source bash/utils.inc.sh
source bash/functions.inc.sh

source bash/010_uninstaller.inc.sh

get_arguments $*

logFile "-------------- Starting CentralReport installer  --------------"

clear

printBox blue  "-------------------------- CentralReport installer ----------------------------| \
                | \
                Welcome! This script will install CentralReport on your host.| \
                If you want more details, | \
                please visit http://github.com/CentralReport/CentralReport| \
                | \
                When installing CentralReport, we may ask for your password.| \
                It will allow CentralReport to write files and directories such as| \
                the project binaries, logs, etc."

# Right now, CentralReport is only available on Mac OS X, Debian and Ubuntu.
# Others Linux distributions coming soon.
getOS
if [ ${CURRENT_OS} != ${OS_MAC} ] && [ ${CURRENT_OS} != ${OS_DEBIAN} ]; then
    printBox red "ERROR!| \
                  The install is only designed for Mac OS, Debian and Ubuntu.| \
                  Support for other OS will come soon!"

    exit 1
fi

# Python is mandatory for CentralReport
check_python
RETURN_PYTHON_CHECK="$?"
if [ "${RETURN_PYTHON_CHECK}" -eq 1 ]; then
    printBox red "Error! Python must be installed on your host to execute CentralReport."
    exit 1
elif [ "${RETURN_PYTHON_CHECK}" -eq 2 ]; then
    printBox red "Error! CentralReport is only designed to work with Python 2.6 or newer."
    exit 1
elif [ "${RETURN_PYTHON_CHECK}" -eq 3 ]; then
    printBox red "Error! CentralReport doesn't work with Python 3.0 or newer!"
    exit 1
fi

# On debian, the current user must have administrative privileges.
if [ ${CURRENT_OS} == ${OS_DEBIAN} ]; then
    if [[ $EUID -ne 0 ]]; then
        ROOT_ERROR="You must be root to install CentralReport!"
        logFile ${ROOT_ERROR}
        printBox red ${ROOT_ERROR}
        exit 1
    fi
fi

# Before installing, we must check if an old version of CentralReport is already installed
detect_010_version
if [ "$?" -ne 0 ]; then
    printBox yellow "CentralReport 0.1.0 has been detected on your host.| \
                     Before installing the new version, we must delete it. This is automatic,| \
                     but your configuration file will be erased. You can do a backup before if| \
                     you want. The configuration file is: /etc/centralreport/centralreport.cfg"
fi

if [ "${ARG_WRONG}" == true ]; then
    printBox red "ERROR! Unknown argument| \
                  Use: install.sh [-s]"
else
    INSTALL_CONFIRMED=false

    # The "-s" argument allows silent installation without any user interaction
    if [ "${ARG_S}" == true ]; then
        INSTALL_CONFIRMED=true
    else
        logConsole " "
        read -p "You will install CentralReport. Are you sure you want to continue? (y/N) " RESP < /dev/tty
        checkYesNoAnswer ${RESP}

        if [ $? -eq 0 ]; then
            INSTALL_CONFIRMED=true
        fi
    fi

    if [ "${INSTALL_CONFIRMED}" == true ]; then
        bit_error=0

        if [ ${CURRENT_OS} == ${OS_MAC} ]; then
            logInfo "Processing... CentralReport will be installed on this Mac."

            # On Mac OS, the user must have access to administrative commands.
            # Checking whether the "sudo" session is still alive...
            sudo -n echo "hey" > /dev/null 2>&1
            if [ "$?" -ne 0 ]; then

                echo -e "\n\nPlease use your administrator password to install CentralReport on this Mac."
                sudo -v
                if [ $? -ne 0 ]; then
                    logError "Unable to use root privileges!"
                    bit_error=1
                fi
            fi
        elif [ ${CURRENT_OS} == ${OS_DEBIAN} ]; then
            logInfo "Processing... CentralReport will be installed on this Linux."
        fi

        # Process to CentralReport installation...
        if [ ${bit_error} -eq 0 ]; then
            install_cr
            if [ "$?" -ne 0 ]; then
                bit_error=1
            fi
        fi

        if [ ${bit_error} -eq 1 ]; then
            # One or more error(s) append during installation.
            # We display a generic message: previous logs already contain messages about the error.
            logConsole " "
            printBox red "Something went wrong when installing CentralReport!| \
                          CentralReport isn't installed on this host.| \
                          | \
                          Some logs have been written in ${ERROR_FILE}"

            logFile "Something went wrong when installing CentralReport, please consult previous logs."

        else
            # Nothing wrong happened while installing.
            logFile "CentralReport is now installed!"
            logFile "For more options, you can edit the config file at /etc/centralreport/centralreport.cfg"
            logFile "More help at http://github.com/CentralReport/CentralReport. Have fun!"

            # Adding a space before the lightbox to separate previous logs with the success message.
            logConsole " "
            printBox blue "CentralReport is now installed!| \
                           For more options, you can edit the config file| \
                           at /etc/centralreport/centralreport.cfg| \
                           | \
                           You can find more help at http://github.com/CentralReport/CentralReport.| \
                           Have fun!"

        fi
    else
        logInfo "Installation aborted on user demand."
    fi
fi

if [ ${CURRENT_OS} == ${OS_MAC} ]; then
    # Remove sudo privileges
    sudo -k
fi

logFile " -- End of the install program -- "
exit 0
