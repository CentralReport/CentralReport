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
    echo -e "$*" >&1
    logFile "$*"
}

# Writes a title on the standard output and writes the message in the log file
function printTitle() {
    logConsole "------------------------------------------------------------------------------"
    logInfo "$*"
    logConsole "------------------------------------------------------------------------------"
}

# Writes a message on the error output and in the log file
function logError() {
    echo -e "\033[0;31m$*\033[0m" >&2
    logFile "$*"
}
