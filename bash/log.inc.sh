#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

ERROR_FILE="/var/log/centralreport.log"

# Writes a message in the log file
function writeLog() {
    CURRENT_DATE=$(date '+%d/%m/%Y %H:%M:%S')

    echo -e "INSTALL\t ${CURRENT_DATE}\t $*" >> ${ERROR_FILE}
}

# Writes a message on the standard output
function writeConsole() {
    echo -e "$*" >&1
}

# Writes a message on the standard output and in the log file
function writeInfo() {
    echo -e "$*" >&1
    writeLog "$*"
}

# Writes a title on the standard output and writes the message in the log file
function writeTitle() {
    writeConsole "------------------------------------------------------------------------------"
    writeInfo "$*"
    writeConsole "------------------------------------------------------------------------------"
}

# Writes a message on the error output and in the log file
function writeError() {
    echo -e "\033[0;31m$*\033[0m" >&2
    writeLog "$*"
}
