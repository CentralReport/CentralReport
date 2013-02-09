#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux - Log function
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# Logs will be written in this file. Installer or Uninstaller have administrative privileges, we can write in /var/log.
ERROR_FILE="/var/log/centralreport.log"

# Writes a message in the log file
function logFile() {
    CURRENT_DATE=$(date '+%d/%m/%Y %H:%M:%S')
    echo -e "INSTALL\t ${CURRENT_DATE}\t $*" >> ${ERROR_FILE}
}

# Writes a message on the standard output
function logConsole() {
    echo -e "$*" >&1
}

# Writes a message on the standard output and in the log file
function logInfo() {
    logConsole "$*"
    logFile "$*"
}

# Writes a title on the standard output and writes the message in the log file
function printTitle() {
    logConsole "--------------------------------------------------------------------------------"
    logInfo "$*"
    logConsole "--------------------------------------------------------------------------------"
}

# Write a light box on console. Available color : blue
function printLightBox() {

    LIGHTBOX_COLOR="$1"
    LIGHTBOX_TEXT="$2"
    LIGHTBOX_SPACE=" "

    # One lightbox line must contain 80 letters.
    while [ ${#LIGHTBOX_TEXT} -lt 80 ]
    do
        LIGHTBOX_TEXT="${LIGHTBOX_TEXT}${LIGHTBOX_SPACE}"
    done

    if [ ${LIGHTBOX_COLOR} == "blue" ]; then
        LIGHTBOX_TEXT="\033[0;44m${LIGHTBOX_TEXT}\033[0m"
    fi

    logConsole "${LIGHTBOX_TEXT}"

}

# Writes a message on the error output and in the log file
function logError() {
    echo -e "\033[0;31m$*\033[0m" >&2
    logFile "$*"
}
