#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux - Log function
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

# Logs will be written in this file, it doesn't require administrative privileges.
ERROR_FILE="/tmp/centralreport_install.log"

#
# Writes a message in the log file
#
# PARAMETERS:
#     $1 = log message
# RETURN: None
#
function logFile() {
    CURRENT_DATE=$(date '+%d/%m/%Y %H:%M:%S')
    echo -e "INSTALL\t ${CURRENT_DATE}\t $*" >> ${ERROR_FILE}
}

#
# Writes a message on the standard output
#
# PARAMETERS:
#     $1 = log message
# RETURN: None
#
function logConsole() {
    echo -e "$*" >&1
}

#
# Writes a message on the standard output and in the log file
#
# PARAMETERS:
#     $1 = log message
# RETURN: None
#
function logInfo() {
    logConsole "$*"
    logFile "$*"
}

#
# Writes a title on the standard output and writes the message in the log file
#
# PARAMETERS:
#     $1 = log message
# RETURN: None
#
function printTitle() {
    logConsole "--------------------------------------------------------------------------------"
    logInfo "$*"
    logConsole "--------------------------------------------------------------------------------"
}

#
# Writes a message on the error output and in the log file
#
# PARAMETERS:
#     $1 = text to trim
# RETURN:
#     The trimmed text
#
function logError() {
    logConsole " "
    echo -e "\033[0;31m$*\033[0m" >&2
    logFile "ERROR: $*"
}

#
# Writes a message in the system log (typically in /var/log/system.log)
# This function doesn't require administrative privileges.
#
# PARAMETERS:
#     $1 = text to trim
# RETURN:
#     The trimmed text
#
function logSystem() {
    logger -t "CentralReport" "$*"
}


#
# Writes a light box on console.
# A lightbox is a line of 80 characters max with the choosen background.
# If your text is less than 80 characters lenght, some spaces will be added to build a full line.
#
# PARAMETERS:
#     $1 = background color : "blue", "yellow" or "red"
#     $2 = the message to display. Be sure that this message is less than 80 characters lenght.
# RETURN: None
#
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
        LIGHTBOX_TEXT="\033[0;44m\033[37m${LIGHTBOX_TEXT}\033[0m"
    elif [ ${LIGHTBOX_COLOR} == "red" ]; then
        LIGHTBOX_TEXT="\033[0;41m\033[37m${LIGHTBOX_TEXT}\033[0m"
    elif [ ${LIGHTBOX_COLOR} == "yellow" ]; then
        LIGHTBOX_TEXT="\033[0;43m\033[30m${LIGHTBOX_TEXT}\033[0m"
    fi

    logConsole "${LIGHTBOX_TEXT}"

}

#
# Remove leading and trailing whitespace of a string
#
# PARAMETERS:
#     $1 = text to trim
# RETURN:
#     The trimmed text
#
function trim() {
    local TEXT="$1"
    TEXT="${TEXT#"${TEXT%%[![:space:]]*}"}"  # remove leading whitespace characters
    TEXT="${TEXT%"${TEXT##*[![:space:]]}"}"  # remove trailing whitespace characters
    echo -n "${TEXT}"
}

#
# Displays a pretty block of text in the color choised
#
# PARAMETERS:
#     $1 = color of the box (red or blue)
#     $2 = message to display
# RETURN:
#     The block of text in the standard output
#
function printBox(){

    LIGHTBOX_COLOR="$1"
    LIGHTBOX_TEXT="$2"

    OIFS=$IFS
    IFS='| '
    IFS=${IFS:0:1}
    TEXT_ARRAY=( ${LIGHTBOX_TEXT} )

    printLightBox ${LIGHTBOX_COLOR} " "
    for LIGNE in "${TEXT_ARRAY[@]}"
    do
        TRIMMED=$(trim ${LIGNE})
        printLightBox ${LIGHTBOX_COLOR} " ${TRIMMED}"
    done
    printLightBox ${LIGHTBOX_COLOR} " "

    IFS=${OIFS};
}
