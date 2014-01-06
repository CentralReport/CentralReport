#!/bin/bash

# ------------------------------------------------------------
# CentralReport Unix/Linux bash functions
# Alpha version. Don't use in production environment!
# ------------------------------------------------------------
# https://github.com/CentralReport
# ------------------------------------------------------------

#
# Gets all script arguments
# The current OS will be stored in "CURRENT_OS" var.
#
# PARAMETERS: None
# RETURN: None
#
function get_arguments(){

    ARG_K=false
    ARG_S=false

    # http://wiki.bash-hackers.org/howto/getopts_tutorial
    while getopts ":ks" opt; do
        case $opt in
            k) ARG_K=true ;;
            s) ARG_S=true ;;
            \?) ARG_WRONG=true ;;
        esac
    done
}

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
    elif [ -f "/etc/redhat-release" ]; then
        OS=`cat /etc/redhat-release | awk {'print $1'}`
#        if [ ${OS} != "CentOS" ]; then
#            CURRENT_OS=${OS_REDHAT}
#        else
#            CURRENT_OS=${OS_CENTOS}
#        fi
        if [ ${OS} == "CentOS" ]; then
            CURRENT_OS=${OS_CENTOS}
        fi
    else
        CURRENT_OS=${OS_OTHER}
    fi
}

#
# Checks whether python is available
#
# PARAMETERS: None
# RETURN:
#   0 = Python is available
#   1 = Python is not available on this host
#   2 = Python version is too old
#   3 = Python version is 3.0 or newer
#
function check_python {

    # Checking Python availability
    python -V &> /dev/null
    if [ "$?" -ne 0 ]; then
        return 1
    fi

    if [ $(python -c 'import sys; print (sys.version_info < (2, 6) and "1" or "0")') -eq 1 ]; then
        return 2
    fi

    if [ $(python -c 'import sys; print (sys.version_info >= (3, 0) and "1" or "0")') -eq 1 ]; then
        return 3
    fi

    return 0
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

    $* 1>/dev/null 2>>${ERROR_FILE}>/dev/null
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
# Executes a privileged command.
#
# PARAMETERS:
#   $1..n: The command to execute
# RETURN:
#   $?: the result of the command
#
function execute_privileged_command() {

    TEST_SUDO=$(which sudo)

    if [ "$?" -eq 0 ]; then
        sudo $*
    else
        # If sudo is not available, we are already connected as root.
        eval "$*"
    fi

    # Returns the result of the executed command
    return "$?"
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
