#!/bin/bash

# CentralReport Unix/Linux Indev version.
# By careful! Don't use in production environment!

function getOS(){
    # Getting actual OS (Linux distrib or Unix OS)
    if [ $(uname -s) == "Darwin" ]; then
        CURRENT_OS=${OS_MAC}
    elif [ -f "/etc/debian_version" ] || [ -f "/etc/lsb-release" ]; then
        CURRENT_OS=${OS_DEBIAN}
    fi
}

function displayError {

    echo -e "\033[1;31m"
    echo $1
    echo -e "\033[0m"

}

function getPythonIsInstalled {

    python -V

    if [ $? -ne 0 ]; then
        return 1
    else
        return 0
    fi

}