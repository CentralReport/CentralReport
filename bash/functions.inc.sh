#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash functions
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/miniche/CentralReport/
# ------------------------------------------------------------

#
# Determines the current OS.
# The current OS will be stored in "CURRENT_OS" var.
#
# PARAMETERS: None
# RETURN: None
#
function getOS(){

    if [ "Darwin" == $(uname -s) ]; then
        CURRENT_OS=${OS_MAC}
    elif [ -f "/etc/debian_version" ] || [ -f "/etc/lsb-release" ]; then
        CURRENT_OS=${OS_DEBIAN}
    fi
}

#
# Displays the python version (if python is available)
#
# PARAMETERS: None
# RETURN:
#   0 = Python is not available on this host
#   1 = Python is available
#
function getPythonIsInstalled {

    echo " "
    python -V &> /dev/null

    if [ $? -ne 0 ]; then
        return 1
    else
        return 0
    fi

}

#
# Displays an error message and exits the current function or program
#
# PARAMETERS:
#   $1 = The error code
#   $2 = The message
# RETURN: None
#
function displayErrorAndExit() {
    local exitcode=$1
    shift
    displayerror "$*"
    exit ${exitcode}
}

#
# Displays the message with current status (.../ERR/OK), while executing the command.
#
# PARAMETERS:
#   $1 = The message to display
#   $2..n = COMMAND (! not |)
# RETURN: None
#
function displayAndExec() {
    local message=$1
    echo -n "[...] ${message}"
    shift

    $* 1>/dev/null 2>ERROR_FILE>/dev/null
    local ret=$?

    if [ ${ret} -ne 0 ]; then
        logFile "[ERR] ${message}"
        echo -e "\r\033[0;31m [ERR]\033[0m ${message}"
    else
        logFile "[OK ] ${message}"
        echo -e "\r\033[0;32m [OK ]\033[0m ${message}"
    fi

    return ${ret}
}

#
# Checks if the answer is "Yes" (y/Y/yes/YES/Yes) or not.
#
# PARAMETERS:
#   $1 = A string to test.
# RETURN:
#   0 = The answer is TRUE
#   1 = The answer is NOT TRUE
#
function checkYesNoAnswer() {

    case "$1" in
        y|Y|yes|YES|Yes) return 0 ;;
        *)  return 1 ;;
    esac

}
