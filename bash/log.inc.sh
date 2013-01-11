#!/bin/bash

# CentralReport Unix/Linux Indev version.
# Be careful! Don't use in production environment!

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
    logInfo "$*"
}
