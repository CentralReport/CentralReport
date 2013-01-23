#!/bin/bash

# CentralReport Unix/Linux Indev version.
# Be careful! Don't use in production environment!

# Gets current OS (Linux distrib or Unix OS)
function getOS(){

    if [ "Darwin" == $(uname -s) ]; then
        CURRENT_OS=${OS_MAC}
    elif [ -f "/etc/debian_version" ] || [ -f "/etc/lsb-release" ]; then
        CURRENT_OS=${OS_DEBIAN}
    fi
}

# Displays the python version (if python is available)
# Returns 0 if python is available, 1 otherwise.
function getPythonIsInstalled {

    echo " "
    python -V

    if [ $? -ne 0 ]; then
        return 1
    else
        return 0
    fi

}

# Displays an error message and exits the current function or program
# First parameter: ERROR CODE
# Second parameter: MESSAGE
function displayErrorAndExit() {
    local exitcode=$1
    shift
    displayerror "$*"
    exit ${exitcode}
}

# Displays the message with current status (.../ERR/OK), while executing the command.
# First parameter: MESSAGE
# Others parameters: COMMAND (! not |)
function displayAndExec() {
    local message=$1
    echo -n "[...] ${message}"
    shift

    echo ">>> $*" >> /dev/null 2>&1
    sh -c "$*" >> /dev/null 2>&1
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


# Verifies if the answer is "Yes" (y/Y/yes/YES/Yes) or not.
# PARAMETER : a string
# Returns 0 if true, 1 otherwise
function verifyYesNoAnswer() {

    case "$1" in
        y|Y|yes|YES|Yes) return 0 ;;
        *) echo Exiting; return 1 ;;
    esac

}
